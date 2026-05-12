"""Report-only simple baselines for UFC Fight Predictor reliability checks."""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from statistics import mean
from typing import Any

from psycopg.rows import dict_row

from ml import backtest
from ml.features import FEATURE_NAMES
from ml.odds_aware_report import american_to_implied_probability, flat_stake_net_profit, remove_vig

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "experiments"
DEFAULT_JSON_OUTPUT = DEFAULT_OUTPUT_DIR / "simple-baselines.json"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_OUTPUT_DIR / "simple-baselines.md"


def run_simple_baselines(
    *,
    start_date: date | None = None,
    end_date: date | None = None,
    max_events: int | None = None,
    output_path: Path = DEFAULT_JSON_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN_OUTPUT,
) -> dict[str, Any]:
    """Evaluate leak-free simple baselines in chronological event order."""
    samples, events = _load_samples(
        start_date=start_date,
        end_date=end_date,
        max_events=max_events,
    )
    events = backtest._target_events(samples, start_date, end_date)
    if max_events is not None:
        events = events[:max_events]
    event_ids = {event["event_id"] for event in events}
    evaluation_samples = [sample for sample in samples if sample["event_id"] in event_ids]
    markets = _load_market_consensus()

    baselines = [
        _evaluate_rule_baseline("ufc_experience", "Pick the fighter with more prior UFC fights.", evaluation_samples, markets, _ufc_experience_probability),
        _evaluate_rule_baseline("recent_form_wins_last_3", "Pick the fighter with more wins in the last 3 prior fights.", evaluation_samples, markets, _recent_form_probability),
        _evaluate_rule_baseline("younger_fighter", "Pick the younger fighter when both dates of birth are available.", evaluation_samples, markets, _younger_fighter_probability),
        _evaluate_market_favorite(evaluation_samples, markets),
    ]
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "simple-baselines",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "value_status_reason": (
            "Baseline ROI is simulated research output until leakage audits, market coverage, "
            "and market-gated validation pass."
        ),
        "chronology": {
            "mode": "walk-forward-compatible chronological event order",
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "max_events": max_events,
            "events_evaluated": len(events),
            "samples_evaluated": len(evaluation_samples),
        },
        "market_coverage": _market_coverage(evaluation_samples, markets),
        "baselines": baselines,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Simple Leak-Free Baselines",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Report-only: `{str(report['report_only']).lower()}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Value status: `{report['value_status']}`",
        f"- Events evaluated: {report['chronology']['events_evaluated']}",
        f"- Samples evaluated: {report['chronology']['samples_evaluated']}",
        f"- Market-covered samples: {report['market_coverage']['covered_samples']}",
        "",
        "## Baselines",
        "",
        "| Baseline | Count | Accuracy | Log loss | Brier | ROC AUC | Sim entries | Sim ROI |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for baseline in report["baselines"]:
        metrics = baseline["metrics"]
        roi = baseline["simulated_research_roi"]
        lines.append(
            "| {name} | {count} | {accuracy} | {log_loss} | {brier} | {roc_auc} | {entries} | {roi} |".format(
                name=baseline["name"],
                count=metrics["count"],
                accuracy=_fmt_pct(metrics["accuracy"]),
                log_loss=_fmt_metric(metrics["log_loss"]),
                brier=_fmt_metric(metrics["brier_score"]),
                roc_auc=_fmt_metric(metrics["roc_auc"]),
                entries=roi["entries"],
                roi=_fmt_pct(roi["roi_pct"]),
            )
        )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            report["value_status_reason"],
            "These baselines do not train, save model files, write `model_versions`, or activate value claims.",
        ]
    )
    return "\n".join(lines)


def _load_samples(
    *,
    start_date: date | None,
    end_date: date | None,
    max_events: int | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [
        row
        for row in backtest._load_completed_fights()
        if end_date is None or row["event_date"] <= end_date
    ]
    candidate_events = _raw_target_events(rows, start_date, end_date)
    if max_events is not None:
        candidate_events = candidate_events[:max_events]
    candidate_event_ids = {event["event_id"] for event in candidate_events}
    sample_rows = [row for row in rows if row["event_id"] in candidate_event_ids]
    samples = backtest._build_samples(sample_rows, FEATURE_NAMES)
    sides = _load_fight_sides([sample["fight_id"] for sample in samples])
    enriched = [{**sample, **sides[sample["fight_id"]]} for sample in samples if sample["fight_id"] in sides]
    return enriched, candidate_events


def _raw_target_events(
    rows: list[dict[str, Any]],
    start_date: date | None,
    end_date: date | None,
) -> list[dict[str, Any]]:
    events_by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if start_date is not None and row["event_date"] < start_date:
            continue
        if end_date is not None and row["event_date"] > end_date:
            continue
        events_by_id[row["event_id"]] = {
            "event_id": row["event_id"],
            "event_name": row["event_name"],
            "event_date": row["event_date"],
        }
    return sorted(events_by_id.values(), key=lambda row: (row["event_date"], row["event_id"]))


def _load_fight_sides(fight_ids: list[str]) -> dict[str, dict[str, str]]:
    if not fight_ids:
        return {}
    from ml.db import pool

    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    fr.fight_id,
                    fr.fighter_id
                FROM fight_results fr
                WHERE fr.fight_id = ANY(%s)
                    AND fr.outcome IN ('win', 'loss')
                ORDER BY fr.fight_id, fr.fighter_id
                """,
                (fight_ids,),
            )
            rows = cur.fetchall()
    by_fight: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        by_fight[str(row["fight_id"])].append(str(row["fighter_id"]))
    return {
        fight_id: {"fighter_a_id": fighter_ids[0], "fighter_b_id": fighter_ids[1]}
        for fight_id, fighter_ids in by_fight.items()
        if len(fighter_ids) == 2
    }


def _evaluate_rule_baseline(
    name: str,
    description: str,
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    probability_fn: Any,
) -> dict[str, Any]:
    predictions = []
    for sample in samples:
        probability = probability_fn(sample)
        predictions.append(_prediction_row(sample, probability))
    return {
        "name": name,
        "description": description,
        "coverage": {"samples": len(predictions), "market_samples": _covered_count(predictions, markets)},
        "metrics": backtest._metrics(predictions),
        "simulated_research_roi": _edge_roi(predictions, markets),
    }


def _evaluate_market_favorite(
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    predictions = []
    for sample in samples:
        market = markets.get(sample["fight_id"])
        if not market:
            continue
        fighter_a_market = market.get(sample["fighter_a_id"])
        if fighter_a_market is None:
            continue
        predictions.append(_prediction_row(sample, fighter_a_market["market_prob"]))
    return {
        "name": "market_favorite",
        "description": "Pick the fighter with higher no-vig market probability where historical odds are matched.",
        "coverage": {"samples": len(predictions), "market_samples": len(predictions)},
        "metrics": backtest._metrics(predictions),
        "simulated_research_roi": _all_pick_roi(predictions, markets),
    }


def _prediction_row(sample: dict[str, Any], fighter_a_probability: float) -> dict[str, Any]:
    probability = min(0.99, max(0.01, fighter_a_probability))
    predicted_label = 1 if probability >= 0.5 else 0
    confidence = probability if predicted_label == 1 else 1 - probability
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "fighter_a_id": sample["fighter_a_id"],
        "fighter_b_id": sample["fighter_b_id"],
        "predicted_label": predicted_label,
        "actual_label": sample["label"],
        "fighter_a_win_prob": probability,
        "confidence": confidence,
        "model_edge": confidence - 0.5,
        "correct": predicted_label == sample["label"],
    }


def _ufc_experience_probability(sample: dict[str, Any]) -> float:
    values = _feature_values(sample)
    diff = values["ufc_fight_count_diff"]
    if math.isnan(diff) or diff == 0:
        return 0.5
    return 0.6 if diff > 0 else 0.4


def _recent_form_probability(sample: dict[str, Any]) -> float:
    values = _feature_values(sample)
    diff = values["wins_last_3_diff"]
    if math.isnan(diff) or diff == 0:
        return 0.5
    adjustment = min(abs(diff), 3.0) * 0.04
    return 0.5 + adjustment if diff > 0 else 0.5 - adjustment


def _younger_fighter_probability(sample: dict[str, Any]) -> float:
    values = _feature_values(sample)
    age_diff = values["age_diff"]
    if math.isnan(age_diff) or age_diff == 0:
        return 0.5
    return 0.55 if age_diff < 0 else 0.45


def _feature_values(sample: dict[str, Any]) -> dict[str, float]:
    return dict(zip(FEATURE_NAMES, sample["features"], strict=True))


def _load_market_consensus() -> dict[str, dict[str, dict[str, float]]]:
    from ml.db import pool

    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    hof.canonical_fight_id,
                    hmo.source_offer_id,
                    hmo.canonical_fighter_id,
                    hmo.american_odds,
                    hmo.decimal_odds
                FROM historical_moneyline_odds hmo
                JOIN historical_odds_fights hof ON hof.id = hmo.historical_fight_id
                WHERE hof.match_status = 'matched'
                    AND hof.canonical_fight_id IS NOT NULL
                    AND hmo.canonical_fighter_id IS NOT NULL
                    AND hmo.line_kind = 'source_current'
                ORDER BY hof.canonical_fight_id, hmo.source_offer_id, hmo.canonical_fighter_id
                """
            )
            rows = cur.fetchall()

    by_offer: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_offer[(str(row["canonical_fight_id"]), str(row["source_offer_id"]))].append(row)

    values_by_fight: dict[str, dict[str, dict[str, list[float]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    for (fight_id, _offer_id), offer_rows in by_offer.items():
        distinct = {row["canonical_fighter_id"]: row for row in offer_rows}
        if len(distinct) != 2:
            continue
        [left, right] = distinct.values()
        left_prob, right_prob = remove_vig(
            american_to_implied_probability(int(left["american_odds"])),
            american_to_implied_probability(int(right["american_odds"])),
        )
        for row, no_vig in [(left, left_prob), (right, right_prob)]:
            fighter_id = str(row["canonical_fighter_id"])
            values_by_fight[fight_id][fighter_id]["market_prob"].append(no_vig)
            values_by_fight[fight_id][fighter_id]["decimal_odds"].append(float(row["decimal_odds"]))

    consensus: dict[str, dict[str, dict[str, float]]] = {}
    for fight_id, fighter_values in values_by_fight.items():
        if len(fighter_values) != 2:
            continue
        consensus[fight_id] = {
            fighter_id: {
                "market_prob": mean(values["market_prob"]),
                "decimal_odds": mean(values["decimal_odds"]),
            }
            for fighter_id, values in fighter_values.items()
        }
    return consensus


def _edge_roi(
    predictions: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    entries = []
    for prediction in predictions:
        market = markets.get(prediction["fight_id"])
        if not market:
            continue
        pick = _pick_side(prediction)
        pick_market = market.get(pick["fighter_id"])
        if pick_market is None:
            continue
        edge = pick["probability"] - pick_market["market_prob"]
        if edge <= 0:
            continue
        entries.append(flat_stake_net_profit(pick_market["decimal_odds"], pick["won"]))
    return _roi_summary(entries)


def _all_pick_roi(
    predictions: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    entries = []
    for prediction in predictions:
        market = markets.get(prediction["fight_id"])
        if not market:
            continue
        pick = _pick_side(prediction)
        pick_market = market.get(pick["fighter_id"])
        if pick_market is None:
            continue
        entries.append(flat_stake_net_profit(pick_market["decimal_odds"], pick["won"]))
    return _roi_summary(entries)


def _pick_side(prediction: dict[str, Any]) -> dict[str, Any]:
    picked_a = prediction["predicted_label"] == 1
    return {
        "fighter_id": prediction["fighter_a_id"] if picked_a else prediction["fighter_b_id"],
        "probability": prediction["fighter_a_win_prob"] if picked_a else 1 - prediction["fighter_a_win_prob"],
        "won": prediction["actual_label"] == prediction["predicted_label"],
    }


def _roi_summary(entries: list[float]) -> dict[str, Any]:
    units = sum(entries)
    return {
        "entries": len(entries),
        "units": units,
        "roi_pct": units / len(entries) if entries else None,
        "stake_unit": "flat_1u",
        "status": "simulated_research_only",
    }


def _market_coverage(
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    covered = sum(1 for sample in samples if sample["fight_id"] in markets)
    return {
        "samples": len(samples),
        "covered_samples": covered,
        "coverage_rate": covered / len(samples) if samples else None,
    }


def _covered_count(
    predictions: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> int:
    return sum(1 for prediction in predictions if prediction["fight_id"] in markets)


def _fmt_metric(value: float | None) -> str:
    return "" if value is None else f"{value:.4f}"


def _fmt_pct(value: float | None) -> str:
    return "" if value is None else f"{value * 100:.1f}%"


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run simple leak-free UFC predictor baselines")
    parser.add_argument("--start-date", type=date.fromisoformat, default=None)
    parser.add_argument("--end-date", type=date.fromisoformat, default=None)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_simple_baselines(
        start_date=args.start_date,
        end_date=args.end_date,
        max_events=args.max_events,
        output_path=output_path,
        markdown_path=markdown_path,
    )
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "chronology": report["chronology"],
        "market_coverage": report["market_coverage"],
        "baselines": [
            {
                "name": baseline["name"],
                "metrics": baseline["metrics"],
                "simulated_research_roi": baseline["simulated_research_roi"],
            }
            for baseline in report["baselines"]
        ],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
