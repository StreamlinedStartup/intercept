"""Report-only pre-fight feature availability signal experiment."""
from __future__ import annotations

import argparse
import json
import warnings
from collections.abc import Callable
from datetime import UTC, datetime
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
from ml.market_residual_analysis import (
    _confidence_bucket,
    _feature_availability_bucket,
    _odds_range_bucket,
    _prediction_fields,
)
from ml.model_family_experiments import _eligible_evaluation_samples, _evaluation_events, _xgboost
from ml.odds_aware_report import _load_source_coverage
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-signal-experiment.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-signal-experiment.md"

AVAILABILITY_FEATURE_NAMES = [
    "feature_missing_count",
    "feature_missing_rate",
    "has_recent_form_context",
    "has_weight_context",
]


def run_market_signal_experiment(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> dict[str, Any]:
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    eligible_samples = _eligible_evaluation_samples(samples, 100)
    markets = _load_market_consensus()
    baseline_predictions = _model_predictions(samples, eligible_samples, markets, _base_features)
    candidate_predictions = _model_predictions(samples, eligible_samples, markets, _availability_augmented_features)
    market_predictions = [_market_prediction(sample, markets) for sample in eligible_samples]
    reports = {
        "market_favorite": _strategy_report("market_favorite", market_predictions),
        "xgboost_current": _strategy_report("xgboost_current", baseline_predictions),
        "xgboost_feature_availability": _strategy_report("xgboost_feature_availability", candidate_predictions),
    }
    candidate = reports["xgboost_feature_availability"]
    market = reports["market_favorite"]
    baseline = reports["xgboost_current"]
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-signal-experiment",
        "epic": "intercept-b6yf",
        "task": "intercept-fypt",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "input_candidates": "data/experiments/market-residual-signal-candidates.json",
        "signal": {
            "name": "pre_fight_feature_availability_flags",
            "base_feature_count": len(FEATURE_NAMES),
            "added_feature_names": AVAILABILITY_FEATURE_NAMES,
            "candidate_feature_count": len(FEATURE_NAMES) + len(AVAILABILITY_FEATURE_NAMES),
            "leakage_status": "pre_fight_only",
        },
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
            "model_eligible_events": len({sample["event_id"] for sample in eligible_samples}),
            "model_eligible_fights": len(eligible_samples),
        },
        "strategies": list(reports.values()),
        "deltas": {
            "candidate_vs_market": _strategy_delta(candidate, market),
            "candidate_vs_current_model": _strategy_delta(candidate, baseline),
        },
        "target_cluster_checks": _target_cluster_checks(candidate_predictions, market_predictions),
        "recommendation": _recommendation(candidate, baseline, market),
        "policy": "This experiment is report-only and does not write active model_versions or activate betting/value claims.",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Market Signal Experiment",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Signal: `{report['signal']['name']}`",
        f"- Model-eligible events: {report['coverage']['model_eligible_events']}",
        f"- Model-eligible fights: {report['coverage']['model_eligible_fights']}",
        "",
        "## Strategy Comparison",
        "",
        "| Strategy | Count | Accuracy | Log loss | Brier | ROI |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for strategy in report["strategies"]:
        metrics = strategy["metrics"]
        roi = strategy["simulated_research_roi"]
        lines.append(
            "| {name} | {count} | {accuracy} | {log_loss} | {brier} | {roi} |".format(
                name=strategy["name"],
                count=metrics["count"],
                accuracy=_fmt_pct(metrics["accuracy"]),
                log_loss=_fmt_metric(metrics["log_loss"]),
                brier=_fmt_metric(metrics["brier_score"]),
                roi=_fmt_pct(roi["roi_pct"]),
            )
        )
    lines.extend(
        [
            "",
            "## Deltas",
            "",
            f"- Candidate ROI delta vs market: {_fmt_signed_pct(report['deltas']['candidate_vs_market']['roi_delta'])}",
            f"- Candidate log-loss delta vs market: {_fmt_metric(report['deltas']['candidate_vs_market']['log_loss_delta'])}",
            f"- Candidate Brier delta vs market: {_fmt_metric(report['deltas']['candidate_vs_market']['brier_delta'])}",
            f"- Candidate ROI delta vs current model: {_fmt_signed_pct(report['deltas']['candidate_vs_current_model']['roi_delta'])}",
            f"- Candidate log-loss delta vs current model: {_fmt_metric(report['deltas']['candidate_vs_current_model']['log_loss_delta'])}",
            f"- Candidate Brier delta vs current model: {_fmt_metric(report['deltas']['candidate_vs_current_model']['brier_delta'])}",
            "",
            "## Target Cluster Checks",
            "",
            "| Cluster | Count | Candidate acc | Market acc | Candidate ROI | Market ROI | ROI delta |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for check in report["target_cluster_checks"]:
        candidate = check["candidate"]
        market = check["market"]
        lines.append(
            "| {cluster} | {count} | {candidate_acc} | {market_acc} | {candidate_roi} | {market_roi} | {roi_delta} |".format(
                cluster=check["cluster"],
                count=candidate["metrics"]["count"],
                candidate_acc=_fmt_pct(candidate["metrics"]["accuracy"]),
                market_acc=_fmt_pct(market["metrics"]["accuracy"]),
                candidate_roi=_fmt_pct(candidate["simulated_research_roi"]["roi_pct"]),
                market_roi=_fmt_pct(market["simulated_research_roi"]["roi_pct"]),
                roi_delta=_fmt_signed_pct(check["roi_delta_vs_market"]),
            )
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"- Status: `{report['recommendation']['status']}`",
            f"- Reason: {report['recommendation']['reason']}",
            "",
            "## Policy",
            "",
            report["policy"],
        ]
    )
    return "\n".join(lines)


def _model_predictions(
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    feature_fn: Callable[[dict[str, Any]], np.ndarray],
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    for event in _evaluation_events(evaluation_samples):
        train_samples = [sample for sample in training_samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in evaluation_samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < 100 or not target_samples:
            continue
        model = _xgboost()
        train_x = np.vstack([feature_fn(sample) for sample in train_samples])
        train_y = np.array([sample["label"] for sample in train_samples], dtype=int)
        model.fit(train_x, train_y)
        target_x = np.vstack([feature_fn(sample) for sample in target_samples])
        probabilities = model.predict_proba(target_x)[:, 1]
        predictions.extend(
            _model_prediction(sample, markets, float(probability))
            for sample, probability in zip(target_samples, probabilities, strict=True)
        )
    return predictions


def _model_prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    probability: float,
) -> dict[str, Any]:
    prediction = _prediction_fields(sample, markets[sample["fight_id"]], probability)
    market = markets[sample["fight_id"]]
    return {
        **_prediction_metric_row(sample, prediction),
        "sample": sample,
        "features": _feature_values(sample),
        "market_pick_probability": max(
            market[sample["fighter_a_id"]]["market_prob"],
            market[sample["fighter_b_id"]]["market_prob"],
        ),
    }


def _market_prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    probability = market[sample["fighter_a_id"]]["market_prob"]
    prediction = _prediction_fields(sample, market, probability)
    return {
        **_prediction_metric_row(sample, prediction),
        "sample": sample,
        "features": _feature_values(sample),
        "market_pick_probability": max(
            market[sample["fighter_a_id"]]["market_prob"],
            market[sample["fighter_b_id"]]["market_prob"],
        ),
    }


def _prediction_metric_row(sample: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "weight_class": sample["weight_class"] or "unknown",
        "fighter_a_probability": prediction["fighter_a_probability"],
        "actual_label": sample["label"],
        "predicted_label": prediction["predicted_label"],
        "confidence": prediction["confidence"],
        "won": prediction["won"],
        "decimal_odds": prediction["decimal_odds"],
        "net_profit": prediction["net_profit"],
    }


def _base_features(sample: dict[str, Any]) -> np.ndarray:
    return sample["features"]


def _availability_augmented_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate([sample["features"], _availability_features(sample)])


def _availability_features(sample: dict[str, Any]) -> np.ndarray:
    values = _feature_values(sample)
    missing_count = sum(1 for value in values.values() if np.isnan(value))
    missing_rate = missing_count / len(values)
    has_recent_form = _has_values(values, ["wins_last_3_diff", "wins_last_5_diff"])
    has_weight_context = _has_values(values, ["weight_class_change", "same_weight_class_count_diff"])
    return np.array(
        [
            float(missing_count),
            float(missing_rate),
            1.0 if has_recent_form else 0.0,
            1.0 if has_weight_context else 0.0,
        ],
        dtype=float,
    )


def _has_values(values: dict[str, float], names: list[str]) -> bool:
    return all(not np.isnan(values[name]) for name in names)


def _strategy_report(name: str, predictions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": name,
        "metrics": _safe_metrics(predictions),
        "simulated_research_roi": _roi(predictions),
    }


def _strategy_delta(candidate: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "accuracy_delta": _delta(candidate["metrics"]["accuracy"], baseline["metrics"]["accuracy"]),
        "roi_delta": _delta(
            candidate["simulated_research_roi"]["roi_pct"],
            baseline["simulated_research_roi"]["roi_pct"],
        ),
        "log_loss_delta": _delta(candidate["metrics"]["log_loss"], baseline["metrics"]["log_loss"]),
        "brier_delta": _delta(candidate["metrics"]["brier_score"], baseline["metrics"]["brier_score"]),
    }


def _target_cluster_checks(
    candidate_predictions: list[dict[str, Any]],
    market_predictions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    market_by_fight = {prediction["fight_id"]: prediction for prediction in market_predictions}
    checks = [
        ("feature_availability:sparse", lambda row: _feature_availability_bucket(_cluster_row(row)) == "sparse"),
        ("confidence:model_70_plus", lambda row: _confidence_bucket(_cluster_row(row)) == "model_70_plus"),
        ("odds_range:heavy_favorite_75_plus", lambda row: _odds_range_bucket(_cluster_row(row)) == "heavy_favorite_75_plus"),
    ]
    output = []
    for name, predicate in checks:
        candidate_rows = [row for row in candidate_predictions if predicate(row)]
        market_rows = [market_by_fight[row["fight_id"]] for row in candidate_rows if row["fight_id"] in market_by_fight]
        candidate_report = _strategy_report("candidate", candidate_rows)
        market_report = _strategy_report("market", market_rows)
        output.append(
            {
                "cluster": name,
                "candidate": candidate_report,
                "market": market_report,
                "roi_delta_vs_market": _delta(
                    candidate_report["simulated_research_roi"]["roi_pct"],
                    market_report["simulated_research_roi"]["roi_pct"],
                ),
            }
        )
    return output


def _cluster_row(prediction: dict[str, Any]) -> dict[str, Any]:
    values = prediction["features"]
    missing_count = sum(1 for value in values.values() if np.isnan(value))
    return {
        "weight_class": prediction["weight_class"],
        "model": {"confidence": prediction["confidence"], "predicted_label": prediction["predicted_label"]},
        "features": {
            "missing_count": missing_count,
            "missing_rate": missing_count / len(values),
            "has_recent_form": _has_values(values, ["wins_last_3_diff", "wins_last_5_diff"]),
            "has_weight_context": _has_values(values, ["weight_class_change", "same_weight_class_count_diff"]),
            "has_physical_profile": _has_values(values, ["height_diff", "reach_diff", "age_diff"]),
            "has_common_opponents": _has_values(values, ["common_opponent_count", "common_opponent_win_diff"]),
        },
        "odds": {"market_pick_probability": prediction["market_pick_probability"]},
    }


def _recommendation(candidate: dict[str, Any], baseline: dict[str, Any], market: dict[str, Any]) -> dict[str, str]:
    candidate_vs_baseline = _strategy_delta(candidate, baseline)
    candidate_vs_market = _strategy_delta(candidate, market)
    if (
        candidate_vs_baseline["log_loss_delta"] is not None
        and candidate_vs_baseline["log_loss_delta"] <= 0
        and candidate_vs_baseline["brier_delta"] is not None
        and candidate_vs_baseline["brier_delta"] <= 0
    ):
        return {
            "status": "keep_for_followup",
            "reason": "Candidate did not degrade log loss or Brier versus current model; continue only through market-gated follow-up.",
        }
    return {
        "status": "do_not_promote",
        "reason": (
            "Candidate remains behind the market favorite and does not improve both log loss and Brier versus "
            f"the current model (ROI delta vs market {_fmt_signed_pct(candidate_vs_market['roi_delta'])})."
        ),
    }


def _safe_metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        return _metrics(predictions)


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run report-only feature availability signal experiment")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_market_signal_experiment(output_path=output_path, markdown_path=markdown_path)
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "coverage": report["coverage"],
        "deltas": report["deltas"],
        "recommendation": report["recommendation"],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
