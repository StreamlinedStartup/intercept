"""Report-only post-event evaluation for market indicator snapshots."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "indicator-evaluation.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "indicator-evaluation.md"


def run_indicator_evaluation(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> dict[str, Any]:
    from ml.db import pool

    with pool.borrow() as conn:
        rows = _load_snapshot_results(conn)
    report = build_indicator_evaluation_report(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def build_indicator_evaluation_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = []
    skipped = []
    for row in rows:
        label = target_label(row)
        if label is None:
            skipped.append({"fight_id": row["fight_id"], "target": row["target"], "reason": "label_unavailable"})
            continue
        probability = row.get("model_probability")
        if probability is None:
            skipped.append({"fight_id": row["fight_id"], "target": row["target"], "reason": "model_probability_missing"})
            continue
        predicted = 1 if float(probability) >= 0.5 else 0
        evaluated.append(
            {
                **row,
                "actual_label": label,
                "predicted_label": predicted,
                "hit": predicted == label,
            }
        )

    by_target = {}
    for target in sorted({str(row["target"]) for row in rows}):
        target_rows = [row for row in evaluated if row["target"] == target]
        source_rows = [row for row in rows if row["target"] == target]
        by_target[target] = _target_summary(target_rows, source_rows)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-indicator-post-event-evaluation",
        "report_only": True,
        "writes_model_versions": False,
        "activates_betting": False,
        "summary": {
            "snapshots": len(rows),
            "evaluated": len(evaluated),
            "skipped": len(skipped),
            "targets": len(by_target),
        },
        "targets": by_target,
        "skipped": skipped[:100],
        "limitations": [
            "Evaluation only includes snapshots whose fights have resolved method/round data.",
            "ROI is not treated as production proof; this report is a post-event monitoring artifact.",
            "Sparse prop-market coverage can dominate missing-edge and stale/missing-data rates.",
        ],
    }


def _target_summary(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    probabilities = [float(row["model_probability"]) for row in rows]
    labels = [int(row["actual_label"]) for row in rows]
    hits = sum(1 for row in rows if row["hit"])
    candidates = [row for row in rows if row.get("candidate")]
    edges = [float(row["edge_pct"]) for row in rows if row.get("edge_pct") is not None]
    candidate_edges = [float(row["edge_pct"]) for row in candidates if row.get("edge_pct") is not None]
    value_status_counts = Counter(str(row.get("value_status") or "unknown") for row in source_rows)
    stale_or_missing = sum(
        value_status_counts[status] for status in ["missing_snapshot", "stale_snapshot", "insufficient_coverage"]
    )
    return {
        "snapshots": len(source_rows),
        "evaluated": len(rows),
        "coverage": len(rows) / len(source_rows) if source_rows else 0,
        "hit_rate": hits / len(rows) if rows else None,
        "brier_score": _brier(probabilities, labels),
        "avg_model_probability": _mean(probabilities),
        "candidate_count": len(candidates),
        "candidate_hit_rate": sum(1 for row in candidates if row["hit"]) / len(candidates) if candidates else None,
        "avg_edge_pct": _mean(edges),
        "avg_candidate_edge_pct": _mean(candidate_edges),
        "calibration_buckets": _calibration_buckets(probabilities, labels),
        "stale_missing_rate": stale_or_missing / len(source_rows) if source_rows else 0,
        "value_status_counts": dict(value_status_counts),
    }


def target_label(row: dict[str, Any]) -> int | None:
    target = str(row["target"])
    method = str(row.get("method") or "").lower()
    if not method:
        return None
    is_decision = "decision" in method
    if target == "decision":
        return 1 if is_decision else 0
    if target == "finish":
        return 0 if is_decision else 1
    if target == "ko_tko":
        return 1 if "ko" in method or "tko" in method else 0
    if target == "submission":
        return 1 if "sub" in method else 0
    if target.startswith("over_"):
        threshold = _threshold_from_target(target)
        elapsed = elapsed_rounds(
            row.get("round"),
            row.get("time_seconds"),
            row.get("scheduled_rounds"),
            is_decision,
        )
        return None if elapsed is None else 1 if elapsed > threshold else 0
    if target.startswith("under_"):
        threshold = _threshold_from_target(target)
        elapsed = elapsed_rounds(
            row.get("round"),
            row.get("time_seconds"),
            row.get("scheduled_rounds"),
            is_decision,
        )
        return None if elapsed is None else 1 if elapsed < threshold else 0
    return None


def elapsed_rounds(
    result_round: Any,
    time_seconds: Any,
    scheduled_rounds: Any,
    decision: bool,
) -> float | None:
    if decision:
        return float(scheduled_rounds or result_round or 0)
    if result_round is None:
        return None
    seconds = float(time_seconds or 0)
    return max(0.0, float(result_round) - 1 + seconds / 300.0)


def _threshold_from_target(target: str) -> float:
    return float(target.removeprefix("over_").removeprefix("under_").replace("_", "."))


def _brier(probabilities: list[float], labels: list[int]) -> float | None:
    if not probabilities:
        return None
    return sum((probability - label) ** 2 for probability, label in zip(probabilities, labels, strict=True)) / len(
        probabilities
    )


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    if any(math.isnan(value) for value in values):
        return None
    return sum(values) / len(values)


def _calibration_buckets(probabilities: list[float], labels: list[int]) -> list[dict[str, Any]]:
    buckets = [
        ("0.00-0.25", 0.0, 0.25),
        ("0.25-0.50", 0.25, 0.5),
        ("0.50-0.75", 0.5, 0.75),
        ("0.75-1.00", 0.75, 1.01),
    ]
    rows = []
    for label, low, high in buckets:
        indexes = [
            index
            for index, probability in enumerate(probabilities)
            if probability >= low and probability < high
        ]
        if not indexes:
            continue
        bucket_probs = [probabilities[index] for index in indexes]
        bucket_labels = [labels[index] for index in indexes]
        rows.append(
            {
                "bucket": label,
                "count": len(indexes),
                "avg_probability": _mean(bucket_probs),
                "actual_rate": _mean([float(value) for value in bucket_labels]),
            }
        )
    return rows


def _load_snapshot_results(conn: Any) -> list[dict[str, Any]]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT DISTINCT ON (mis.fight_id, mis.target, mis.model_version, mis.indicator_name)
                mis.fight_id,
                mis.target,
                mis.model_version,
                mis.indicator_name,
                mis.computed_at,
                mis.model_probability,
                mis.market_probability,
                mis.edge_pct,
                mis.candidate,
                mis.market_pair_count,
                mis.value_status,
                f.scheduled_rounds,
                fr.method,
                fr.round,
                fr.time_seconds
            FROM market_indicator_snapshots mis
            JOIN fights f ON f.id = mis.fight_id
            JOIN fight_results fr ON fr.fight_id = f.id
            WHERE fr.method IS NOT NULL
                AND fr.method <> ''
            ORDER BY
                mis.fight_id,
                mis.target,
                mis.model_version,
                mis.indicator_name,
                mis.computed_at DESC,
                CASE WHEN fr.outcome = 'win' THEN 0 ELSE 1 END
            """,
        )
        return list(cur.fetchall())


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Market Indicator Post-Event Evaluation",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Report only: `{str(report['report_only']).lower()}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Activates betting: `{str(report['activates_betting']).lower()}`",
        f"- Evaluated snapshots: {report['summary']['evaluated']} / {report['summary']['snapshots']}",
        "",
        "## Targets",
        "",
        "| Target | Evaluated | Coverage | Hit rate | Brier | Candidates | Candidate hit rate | Avg edge | Stale/missing |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for target, row in report["targets"].items():
        lines.append(
            "| {target} | {evaluated} | {coverage} | {hit_rate} | {brier} | {candidates} | {candidate_hit_rate} | {avg_edge} | {stale_missing} |".format(
                target=target,
                evaluated=row["evaluated"],
                coverage=_fmt_pct(row["coverage"]),
                hit_rate=_fmt_pct(row["hit_rate"]),
                brier=_fmt(row["brier_score"]),
                candidates=row["candidate_count"],
                candidate_hit_rate=_fmt_pct(row["candidate_hit_rate"]),
                avg_edge=_fmt_signed_pct(row["avg_edge_pct"]),
                stale_missing=_fmt_pct(row["stale_missing_rate"]),
            )
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    return "\n".join(lines)


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def _fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _fmt_signed_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    report = run_indicator_evaluation(output_path=args.output, markdown_path=args.markdown)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
