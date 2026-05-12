"""Report-only high-loss residual cluster analysis."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ml.market_gate_report import _fmt_pct, _fmt_signed_pct, _load_matched_market_samples, _resolve_repo_path
from ml.market_residual_analysis import (
    _bucket_report,
    _confidence_bucket,
    _disagreement_bucket,
    _event_age_bucket,
    _favorite_side_bucket,
    _feature_availability_bucket,
    _odds_range_bucket,
    _residual_rows,
)
from ml.baselines import _load_market_consensus
from ml.odds_aware_report import _load_source_coverage
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-residual-clusters.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-residual-clusters.md"

HIGH_LOSS_ROI_DELTA = -0.25
HIGH_LOSS_ACCURACY_DELTA = -0.20
HIGH_CONF_WRONG_RATE = 0.25


def run_market_residual_clusters(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> dict[str, Any]:
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    rows = _residual_rows(samples, _load_market_consensus())
    latest_event_date = max((row["event_date"] for row in rows), default=None)
    corpus_features = _feature_summary(rows)
    clusters = _failure_clusters(rows, latest_event_date, corpus_features)
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-residual-clusters",
        "epic": "intercept-b6yf",
        "task": "intercept-ty3n",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "input_report": "data/experiments/market-residual-buckets.json",
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
            "model_eligible_events": len({row["event_id"] for row in rows}),
            "model_eligible_fights": len(rows),
        },
        "thresholds": {
            "high_loss_roi_delta": HIGH_LOSS_ROI_DELTA,
            "high_loss_accuracy_delta": HIGH_LOSS_ACCURACY_DELTA,
            "high_conf_wrong_rate": HIGH_CONF_WRONG_RATE,
        },
        "corpus_feature_summary": corpus_features,
        "clusters": clusters,
        "recommendation_policy": (
            "Only stable clusters with actionable pre-fight feature gaps can feed Task D signal candidates. "
            "Market-only and unstable/noise clusters are diagnostic only."
        ),
        "policy": "This report does not write model_versions or activate betting/value claims.",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    lines = [
        "# Market Residual Failure Clusters",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Model-eligible events: {coverage['model_eligible_events']}",
        f"- Model-eligible fights: {coverage['model_eligible_fights']}",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Input report: `{report['input_report']}`",
        "",
        "## High-Loss Clusters",
        "",
        "| Cluster | Fights | Events | Model acc | Market acc | ROI delta | High-conf wrong | Explanation | Actionable gaps |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for cluster in report["clusters"]:
        bucket = cluster["bucket_report"]
        lines.append(
            "| {name} | {count} | {events} | {model_acc} | {market_acc} | {roi_delta} | {wrong_rate} | {explanation} | {gaps} |".format(
                name=f"{cluster['dimension']}:{cluster['bucket']}",
                count=bucket["count"],
                events=bucket["events"],
                model_acc=_fmt_pct(bucket["model"]["metrics"]["accuracy"]),
                market_acc=_fmt_pct(bucket["market"]["metrics"]["accuracy"]),
                roi_delta=_fmt_signed_pct(bucket["deltas"]["roi_model_minus_market"]),
                wrong_rate=_fmt_pct(cluster["failure_profile"]["high_conf_wrong_rate"]),
                explanation=cluster["classification"],
                gaps=", ".join(cluster["actionable_feature_gaps"]) or "none",
            )
        )
    lines.extend(
        [
            "",
            "## Feature Baseline",
            "",
            f"- Corpus average missing rate: {_fmt_pct(report['corpus_feature_summary']['average_missing_rate'])}",
            f"- Corpus recent-form availability: {_fmt_pct(report['corpus_feature_summary']['availability_rates']['has_recent_form'])}",
            f"- Corpus physical-profile availability: {_fmt_pct(report['corpus_feature_summary']['availability_rates']['has_physical_profile'])}",
            f"- Corpus weight-context availability: {_fmt_pct(report['corpus_feature_summary']['availability_rates']['has_weight_context'])}",
            f"- Corpus common-opponent availability: {_fmt_pct(report['corpus_feature_summary']['availability_rates']['has_common_opponents'])}",
            "",
            "## Recommendation Policy",
            "",
            report["recommendation_policy"],
            report["policy"],
        ]
    )
    return "\n".join(lines)


def _failure_clusters(
    rows: list[dict[str, Any]],
    latest_event_date: str | None,
    corpus_features: dict[str, Any],
) -> list[dict[str, Any]]:
    dimensions: list[tuple[str, Callable[[dict[str, Any]], str]]] = [
        ("favorite_underdog_side", _favorite_side_bucket),
        ("odds_range", _odds_range_bucket),
        ("weight_class", lambda row: row["weight_class"]),
        ("event_date_age", lambda row: _event_age_bucket(row, latest_event_date)),
        ("feature_availability", _feature_availability_bucket),
        ("confidence", _confidence_bucket),
        ("market_model_disagreement", _disagreement_bucket),
    ]
    clusters = []
    for dimension, key_fn in dimensions:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[key_fn(row)].append(row)
        for bucket, bucket_rows in grouped.items():
            cluster = _cluster_report(dimension, bucket, bucket_rows, corpus_features)
            if _is_high_loss_cluster(cluster):
                clusters.append(cluster)
    return sorted(clusters, key=_cluster_sort_key)


def _cluster_report(
    dimension: str,
    bucket: str,
    rows: list[dict[str, Any]],
    corpus_features: dict[str, Any],
) -> dict[str, Any]:
    bucket_report = _bucket_report(dimension, bucket, rows)
    cluster_features = _feature_summary(rows)
    wrong_rows = [row for row in rows if not row["model"]["won"]]
    wrong_features = _feature_summary(wrong_rows)
    actionable_gaps = _actionable_feature_gaps(cluster_features, corpus_features)
    return {
        "dimension": dimension,
        "bucket": bucket,
        "bucket_report": bucket_report,
        "failure_profile": {
            "model_wrong_market_correct_count": sum(
                1 for row in rows if not row["model"]["won"] and row["market"]["won"]
            ),
            "high_conf_wrong_count": sum(
                1 for row in rows if row["model"]["confidence"] >= 0.65 and not row["model"]["won"]
            ),
            "high_conf_wrong_rate": _ratio(
                sum(1 for row in rows if row["model"]["confidence"] >= 0.65 and not row["model"]["won"]),
                len(rows),
            ),
        },
        "feature_comparison": {
            "corpus": corpus_features,
            "cluster": cluster_features,
            "model_wrong_subset": wrong_features,
        },
        "actionable_feature_gaps": actionable_gaps,
        "classification": _classification(bucket_report, actionable_gaps),
    }


def _is_high_loss_cluster(cluster: dict[str, Any]) -> bool:
    bucket = cluster["bucket_report"]
    deltas = bucket["deltas"]
    if bucket["unstable"]:
        return (
            deltas["roi_model_minus_market"] is not None
            and deltas["roi_model_minus_market"] <= HIGH_LOSS_ROI_DELTA
        )
    if deltas["roi_model_minus_market"] is not None and deltas["roi_model_minus_market"] <= HIGH_LOSS_ROI_DELTA:
        return True
    if (
        deltas["accuracy_model_minus_market"] is not None
        and deltas["accuracy_model_minus_market"] <= HIGH_LOSS_ACCURACY_DELTA
    ):
        return True
    return cluster["failure_profile"]["high_conf_wrong_rate"] >= HIGH_CONF_WRONG_RATE


def _classification(bucket: dict[str, Any], actionable_gaps: list[str]) -> str:
    if bucket["unstable"]:
        return "unstable_or_noise"
    if actionable_gaps:
        return "actionable_pre_fight_feature_gap"
    if bucket["bucket"].startswith("model_on_market_underdog") or bucket["bucket"].startswith("disagree_"):
        return "market_prior_gap"
    return "model_calibration_or_noise"


def _feature_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    flags = ["has_recent_form", "has_physical_profile", "has_weight_context", "has_common_opponents"]
    return {
        "count": len(rows),
        "average_missing_rate": _average([row["features"]["missing_rate"] for row in rows]),
        "average_missing_count": _average([row["features"]["missing_count"] for row in rows]),
        "availability_rates": {
            flag: _ratio(sum(1 for row in rows if row["features"][flag]), len(rows))
            for flag in flags
        },
    }


def _actionable_feature_gaps(cluster_features: dict[str, Any], corpus_features: dict[str, Any]) -> list[str]:
    gaps = []
    if cluster_features["average_missing_rate"] - corpus_features["average_missing_rate"] >= 0.05:
        gaps.append("higher_feature_missingness")
    for name, corpus_rate in corpus_features["availability_rates"].items():
        cluster_rate = cluster_features["availability_rates"][name]
        if corpus_rate - cluster_rate >= 0.10:
            gaps.append(f"lower_{name}")
    return gaps


def _cluster_sort_key(cluster: dict[str, Any]) -> tuple[float, float, str, str]:
    bucket = cluster["bucket_report"]
    roi_delta = bucket["deltas"]["roi_model_minus_market"] or 0.0
    wrong_rate = cluster["failure_profile"]["high_conf_wrong_rate"] or 0.0
    return (roi_delta, -wrong_rate, cluster["dimension"], cluster["bucket"])


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run high-loss market residual cluster analysis")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_market_residual_clusters(output_path=output_path, markdown_path=markdown_path)
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "coverage": report["coverage"],
        "cluster_count": len(report["clusters"]),
        "classifications": {
            name: sum(1 for cluster in report["clusters"] if cluster["classification"] == name)
            for name in sorted({cluster["classification"] for cluster in report["clusters"]})
        },
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
