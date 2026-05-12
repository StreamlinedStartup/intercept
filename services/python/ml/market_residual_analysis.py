"""Report-only model-vs-market residual bucket analysis."""
from __future__ import annotations

import argparse
import json
import math
import warnings
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.exceptions import UndefinedMetricWarning

from ml.baselines import _feature_values, _load_market_consensus
from ml.features import FEATURE_NAMES
from ml.market_gate_report import (
    _fmt_metric,
    _fmt_pct,
    _fmt_signed_pct,
    _load_matched_market_samples,
    _metrics,
    _resolve_repo_path,
    _roi,
)
from ml.model_family_experiments import (
    _eligible_evaluation_samples,
    _evaluation_events,
    _project_matrix,
    _xgboost,
)
from ml.odds_aware_report import _load_source_coverage, flat_stake_net_profit
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-residual-buckets.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-residual-buckets.md"

UNSTABLE_MIN_FIGHTS = 30
UNSTABLE_MIN_EVENTS = 5


def run_market_residual_buckets(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> dict[str, Any]:
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    markets = _load_market_consensus()
    rows = _residual_rows(samples, markets)
    latest_event_date = max((row["event_date"] for row in rows), default=None)
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-residual-buckets",
        "epic": "intercept-b6yf",
        "task": "intercept-h336",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "input_baseline": "data/experiments/market-residual-analysis-baseline.json",
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
            "model_eligible_events": len({row["event_id"] for row in rows}),
            "model_eligible_fights": len(rows),
        },
        "model": {
            "name": "xgboost_current",
            "feature_names": FEATURE_NAMES,
            "split_policy": "Each evaluated event trains only on frozen market-covered fights with event_date before that event.",
        },
        "unstable_bucket_policy": {
            "min_fights": UNSTABLE_MIN_FIGHTS,
            "min_events": UNSTABLE_MIN_EVENTS,
            "recommendation_policy": "unstable buckets are excluded from promotion recommendations",
        },
        "overall": _bucket_report("all", "all", rows),
        "dimensions": _dimensions(rows, latest_event_date),
        "policy": (
            "Residual buckets are diagnostic research artifacts only. They do not activate value status, "
            "publish betting claims, write model_versions, or create promotion recommendations."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    lines = [
        "# Market Residual Bucket Report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Scored events: {coverage['scored_events']}",
        f"- Scored fights: {coverage['scored_fights']}",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Input baseline: `{report['input_baseline']}`",
        "",
        "## Unstable Bucket Policy",
        "",
        f"Buckets with fewer than {report['unstable_bucket_policy']['min_fights']} fights or fewer than {report['unstable_bucket_policy']['min_events']} events are flagged unstable and excluded from promotion recommendations.",
        "",
        "## Overall",
        "",
        _bucket_markdown_row_header(),
        _bucket_markdown_separator(),
        _bucket_markdown_row(report["overall"]),
    ]
    for dimension in report["dimensions"]:
        lines.extend(
            [
                "",
                f"## {dimension['label']}",
                "",
                _bucket_markdown_row_header(),
                _bucket_markdown_separator(),
            ]
        )
        lines.extend(_bucket_markdown_row(bucket) for bucket in dimension["buckets"])
    lines.extend(["", "## Policy", "", report["policy"]])
    return "\n".join(lines)


def _residual_row(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    model_probability: float,
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    market_probability = market[sample["fighter_a_id"]]["market_prob"]
    model = _prediction_fields(sample, market, model_probability)
    market_prediction = _prediction_fields(sample, market, market_probability)
    values = _feature_values(sample)
    market_pick_probability = _pick_probability(market_prediction, market_probability)
    model_pick_probability = _pick_probability(model, model_probability)
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "weight_class": sample["weight_class"] or "unknown",
        "actual_label": sample["label"],
        "model": model,
        "market": market_prediction,
        "odds": {
            "fighter_a_market_probability": market_probability,
            "fighter_b_market_probability": 1 - market_probability,
            "market_pick_probability": market_pick_probability,
        },
        "residuals": {
            "fighter_a_probability_delta_model_minus_market": model_probability - market_probability,
            "pick_probability_delta_model_minus_market": model_pick_probability - market_pick_probability,
            "absolute_probability_delta": abs(model_probability - market_probability),
            "model_market_disagree": model["predicted_label"] != market_prediction["predicted_label"],
        },
        "features": {
            "missing_count": _missing_feature_count(values),
            "missing_rate": _missing_feature_rate(values),
            "has_recent_form": _has_values(values, ["wins_last_3_diff", "wins_last_5_diff"]),
            "has_physical_profile": _has_values(values, ["height_diff", "reach_diff", "age_diff"]),
            "has_weight_context": _has_values(values, ["weight_class_change", "same_weight_class_count_diff"]),
            "has_common_opponents": _has_values(values, ["common_opponent_count", "common_opponent_win_diff"]),
        },
    }


def _prediction_fields(
    sample: dict[str, Any],
    market: dict[str, dict[str, float]],
    fighter_a_probability: float,
) -> dict[str, Any]:
    predicted_label = 1 if fighter_a_probability >= 0.5 else 0
    picked_fighter_id = sample["fighter_a_id"] if predicted_label == 1 else sample["fighter_b_id"]
    pick_market = market[picked_fighter_id]
    won = predicted_label == sample["label"]
    return {
        "fighter_a_probability": fighter_a_probability,
        "predicted_label": predicted_label,
        "confidence": fighter_a_probability if predicted_label == 1 else 1 - fighter_a_probability,
        "picked_fighter_id": picked_fighter_id,
        "won": won,
        "decimal_odds": pick_market["decimal_odds"],
        "net_profit": flat_stake_net_profit(pick_market["decimal_odds"], won),
    }


def _dimensions(rows: list[dict[str, Any]], latest_event_date: str | None) -> list[dict[str, Any]]:
    dimensions: list[tuple[str, str, Callable[[dict[str, Any]], str]]] = [
        ("favorite_underdog_side", "Favorite/Underdog Side", _favorite_side_bucket),
        ("odds_range", "Odds Range", _odds_range_bucket),
        ("weight_class", "Weight Class", lambda row: row["weight_class"]),
        ("event_date_age", "Event Date Age", lambda row: _event_age_bucket(row, latest_event_date)),
        ("feature_availability", "Feature Availability", _feature_availability_bucket),
        ("confidence", "Confidence", _confidence_bucket),
        ("market_model_disagreement", "Market/Model Disagreement", _disagreement_bucket),
    ]
    return [
        {
            "name": name,
            "label": label,
            "buckets": _bucket_dimension(rows, name, key_fn),
        }
        for name, label, key_fn in dimensions
    ]


def _bucket_dimension(
    rows: list[dict[str, Any]],
    dimension: str,
    key_fn: Callable[[dict[str, Any]], str],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[key_fn(row)].append(row)
    return [
        _bucket_report(dimension, key, bucket_rows)
        for key, bucket_rows in sorted(grouped.items(), key=lambda item: item[0])
    ]


def _bucket_report(dimension: str, bucket: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    model_predictions = [_metric_row(row, "model") for row in rows]
    market_predictions = [_metric_row(row, "market") for row in rows]
    event_count = len({row["event_id"] for row in rows})
    unstable_reasons = _unstable_reasons(len(rows), event_count)
    return {
        "dimension": dimension,
        "bucket": bucket,
        "count": len(rows),
        "events": event_count,
        "unstable": bool(unstable_reasons),
        "unstable_reasons": unstable_reasons,
        "eligible_for_promotion_recommendations": not unstable_reasons,
        "model": {
            "metrics": _safe_metrics(model_predictions),
            "simulated_research_roi": _roi(model_predictions),
        },
        "market": {
            "metrics": _safe_metrics(market_predictions),
            "simulated_research_roi": _roi(market_predictions),
        },
        "deltas": _deltas(model_predictions, market_predictions),
    }


def _metric_row(row: dict[str, Any], side: str) -> dict[str, Any]:
    prediction = row[side]
    return {
        "fight_id": row["fight_id"],
        "event_id": row["event_id"],
        "fighter_a_probability": prediction["fighter_a_probability"],
        "actual_label": row["actual_label"],
        "predicted_label": prediction["predicted_label"],
        "confidence": prediction["confidence"],
        "won": prediction["won"],
        "decimal_odds": prediction["decimal_odds"],
        "net_profit": prediction["net_profit"],
    }


def _residual_rows(
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    *,
    min_train_samples: int = 100,
) -> list[dict[str, Any]]:
    eligible_samples = _eligible_evaluation_samples(samples, min_train_samples)
    rows: list[dict[str, Any]] = []
    for event in _evaluation_events(eligible_samples):
        train_samples = [sample for sample in samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in eligible_samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
            continue
        model = _xgboost()
        train_x = _project_matrix(train_samples, FEATURE_NAMES)
        train_y = np.array([sample["label"] for sample in train_samples], dtype=int)
        model.fit(train_x, train_y)
        target_x = _project_matrix(target_samples, FEATURE_NAMES)
        probabilities = model.predict_proba(target_x)[:, 1]
        rows.extend(
            _residual_row(sample, markets, float(probability))
            for sample, probability in zip(target_samples, probabilities, strict=True)
        )
    return rows


def _deltas(model_predictions: list[dict[str, Any]], market_predictions: list[dict[str, Any]]) -> dict[str, Any]:
    model_metrics = _safe_metrics(model_predictions)
    market_metrics = _safe_metrics(market_predictions)
    model_roi = _roi(model_predictions)
    market_roi = _roi(market_predictions)
    return {
        "accuracy_model_minus_market": _delta(model_metrics["accuracy"], market_metrics["accuracy"]),
        "roi_model_minus_market": _delta(model_roi["roi_pct"], market_roi["roi_pct"]),
        "log_loss_model_minus_market": _delta(model_metrics["log_loss"], market_metrics["log_loss"]),
        "brier_model_minus_market": _delta(model_metrics["brier_score"], market_metrics["brier_score"]),
        "calibration_gap_model_minus_market": _delta(
            model_metrics["calibration_gap"],
            market_metrics["calibration_gap"],
        ),
    }


def _safe_metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        return _metrics(predictions)


def _unstable_reasons(count: int, event_count: int) -> list[str]:
    reasons = []
    if count < UNSTABLE_MIN_FIGHTS:
        reasons.append("fewer_than_30_fights")
    if event_count < UNSTABLE_MIN_EVENTS:
        reasons.append("fewer_than_5_events")
    return reasons


def _favorite_side_bucket(row: dict[str, Any]) -> str:
    model_label = row["model"]["predicted_label"]
    market_label = row["market"]["predicted_label"]
    if model_label == market_label:
        return "model_on_market_favorite"
    return "model_on_market_underdog"


def _odds_range_bucket(row: dict[str, Any]) -> str:
    probability = row["odds"]["market_pick_probability"]
    if probability < 0.55:
        return "near_pickem_50_55"
    if probability < 0.65:
        return "favorite_55_65"
    if probability < 0.75:
        return "strong_favorite_65_75"
    return "heavy_favorite_75_plus"


def _event_age_bucket(row: dict[str, Any], latest_event_date: str | None) -> str:
    if latest_event_date is None:
        return "unknown"
    event_date = date.fromisoformat(row["event_date"])
    latest = date.fromisoformat(latest_event_date)
    age_days = (latest - event_date).days
    if age_days < 365:
        return "last_12_months"
    if age_days < 365 * 3:
        return "1_to_3_years"
    if age_days < 365 * 6:
        return "3_to_6_years"
    return "6_plus_years"


def _feature_availability_bucket(row: dict[str, Any]) -> str:
    missing_rate = row["features"]["missing_rate"]
    if missing_rate == 0:
        return "complete"
    if missing_rate <= 0.10:
        return "mostly_complete"
    if missing_rate <= 0.25:
        return "partial"
    return "sparse"


def _confidence_bucket(row: dict[str, Any]) -> str:
    confidence = row["model"]["confidence"]
    if confidence < 0.55:
        return "model_50_55"
    if confidence < 0.60:
        return "model_55_60"
    if confidence < 0.65:
        return "model_60_65"
    if confidence < 0.70:
        return "model_65_70"
    return "model_70_plus"


def _disagreement_bucket(row: dict[str, Any]) -> str:
    delta = row["residuals"]["absolute_probability_delta"]
    prefix = "disagree" if row["residuals"]["model_market_disagree"] else "agree"
    if delta < 0.05:
        return f"{prefix}_delta_0_5pp"
    if delta < 0.10:
        return f"{prefix}_delta_5_10pp"
    if delta < 0.20:
        return f"{prefix}_delta_10_20pp"
    return f"{prefix}_delta_20pp_plus"


def _pick_probability(prediction: dict[str, Any], fighter_a_probability: float) -> float:
    return fighter_a_probability if prediction["predicted_label"] == 1 else 1 - fighter_a_probability


def _missing_feature_count(values: dict[str, float]) -> int:
    return sum(1 for value in values.values() if math.isnan(value))


def _missing_feature_rate(values: dict[str, float]) -> float:
    return _missing_feature_count(values) / len(values) if values else 0.0


def _has_values(values: dict[str, float], names: list[str]) -> bool:
    return all(not math.isnan(values[name]) for name in names)


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def _bucket_markdown_row_header() -> str:
    return "| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |"


def _bucket_markdown_separator() -> str:
    return "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"


def _bucket_markdown_row(bucket: dict[str, Any]) -> str:
    model_metrics = bucket["model"]["metrics"]
    market_metrics = bucket["market"]["metrics"]
    model_roi = bucket["model"]["simulated_research_roi"]
    market_roi = bucket["market"]["simulated_research_roi"]
    return (
        "| {bucket} | {count} | {events} | {stable} | {model_acc} | {market_acc} | {model_roi} | {market_roi} | {roi_delta} | {model_log_loss} | {market_log_loss} | {model_brier} | {market_brier} | {model_cal} | {market_cal} |"
    ).format(
        bucket=bucket["bucket"],
        count=bucket["count"],
        events=bucket["events"],
        stable=str(not bucket["unstable"]).lower(),
        model_acc=_fmt_pct(model_metrics["accuracy"]),
        market_acc=_fmt_pct(market_metrics["accuracy"]),
        model_roi=_fmt_pct(model_roi["roi_pct"]),
        market_roi=_fmt_pct(market_roi["roi_pct"]),
        roi_delta=_fmt_signed_pct(bucket["deltas"]["roi_model_minus_market"]),
        model_log_loss=_fmt_metric(model_metrics["log_loss"]),
        market_log_loss=_fmt_metric(market_metrics["log_loss"]),
        model_brier=_fmt_metric(model_metrics["brier_score"]),
        market_brier=_fmt_metric(market_metrics["brier_score"]),
        model_cal=_fmt_signed_pct(model_metrics["calibration_gap"]),
        market_cal=_fmt_signed_pct(market_metrics["calibration_gap"]),
    )


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model-vs-market residual bucket analysis")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_market_residual_buckets(output_path=output_path, markdown_path=markdown_path)
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "coverage": report["coverage"],
        "overall": report["overall"],
        "dimensions": [
            {"name": dimension["name"], "buckets": len(dimension["buckets"])}
            for dimension in report["dimensions"]
        ],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
