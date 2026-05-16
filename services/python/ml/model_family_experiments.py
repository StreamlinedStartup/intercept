"""Report-only market-scored model-family and feature-ablation experiments."""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from ml.backtest import _confidence_bucket
from ml.baselines import _load_market_consensus
from ml.experiments import (
    COMMON_OPPONENT_FEATURES,
    DAMAGE_FEATURES,
    RECENT_FORM_FEATURES,
    STANCE_FEATURES,
)
from ml.features import FEATURE_NAMES
from ml.market_gate_report import _load_matched_market_samples, _metrics, _roi
from ml.market_blend_experiments import blend_probability, roi_delta
from ml.odds_aware_report import _load_source_coverage, flat_stake_net_profit
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-aware-model-family-experiments.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-aware-model-family-experiments.md"
MIN_TRAIN_SAMPLES = 100
MIN_MARKET_ROI_DELTA = 0.02

type ModelFactory = Callable[[], Any]
type ProbabilityFn = Callable[[float, float], float]


@dataclass(frozen=True)
class ModelVariant:
    name: str
    family: str
    description: str
    feature_names: list[str]
    model_factory: ModelFactory | None
    probability_fn: ProbabilityFn | None = None


def run_model_family_experiments(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
    min_train_samples: int = MIN_TRAIN_SAMPLES,
) -> dict[str, Any]:
    coverage = _load_source_coverage()
    evaluation_samples = _load_matched_market_samples(coverage)
    eligible_samples = _eligible_evaluation_samples(evaluation_samples, min_train_samples)
    markets = _load_market_consensus()
    variants = model_variants()
    reports = [
        _evaluate_market_favorite(eligible_samples, markets),
        *_evaluate_model_variants(
            variants,
            training_samples=evaluation_samples,
            evaluation_samples=eligible_samples,
            markets=markets,
            min_train_samples=min_train_samples,
        ),
    ]
    market = next(report for report in reports if report["name"] == "market_favorite")
    market_roi = market["simulated_research_roi"]["roi_pct"]
    market_metrics = market["metrics"]
    for report in reports:
        _annotate_candidate(report, market_roi, market_metrics)
    candidates = [report for report in reports if report["name"] != "market_favorite"]
    best_candidate = max(
        candidates,
        key=lambda report: report["simulated_research_roi"]["roi_pct"] or float("-inf"),
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-aware-model-family-experiments",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "value_status_reason": (
            "Model-family and feature-ablation candidates remain research-only until a candidate "
            "beats the no-vig market favorite by +2pp without leakage, instability, or calibration degradation."
        ),
        "input_manifest": "data/experiments/market-aware-model-experiment-manifest.json",
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in evaluation_samples}),
            "scored_fights": len(evaluation_samples),
            "model_eligible_events": len({sample["event_id"] for sample in eligible_samples}),
            "model_eligible_fights": len(eligible_samples),
        },
        "training_contract": {
            "min_train_samples": min_train_samples,
            "split_policy": "Each evaluated event trains only on frozen market-covered fights with event_date before that event.",
            "evaluation_policy": "Metrics and ROI are computed only on frozen matched market-covered fights that have enough prior market-covered training samples.",
        },
        "market_baseline": {
            "name": "market_favorite",
            "roi_pct": market_roi,
            "accuracy": market_metrics["accuracy"],
            "log_loss": market_metrics["log_loss"],
            "brier_score": market_metrics["brier_score"],
        },
        "gate": {
            "min_roi_delta_vs_market_favorite": MIN_MARKET_ROI_DELTA,
            "best_candidate": best_candidate["name"],
            "best_candidate_roi_pct": best_candidate["simulated_research_roi"]["roi_pct"],
            "best_candidate_roi_delta_vs_market_favorite": best_candidate["roi_delta_vs_market_favorite"],
            "best_candidate_rejection_reasons": best_candidate["rejection_reasons"],
            "candidate_cleared_gate": best_candidate["clears_market_roi_gate"],
        },
        "variants": reports,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def model_variants() -> list[ModelVariant]:
    baseline = list(FEATURE_NAMES)
    return [
        ModelVariant(
            "xgboost_current",
            "current_model_baseline",
            "Current XGBoost family with production feature set.",
            baseline,
            _xgboost,
        ),
        ModelVariant(
            "blend_25_xgboost_75_market",
            "market_aware_blend",
            "25% current XGBoost probability + 75% no-vig market probability.",
            baseline,
            _xgboost,
            lambda model, market: blend_probability(model, market, 0.25),
        ),
        ModelVariant(
            "blend_50_xgboost_50_market",
            "market_aware_blend",
            "50% current XGBoost probability + 50% no-vig market probability.",
            baseline,
            _xgboost,
            lambda model, market: blend_probability(model, market, 0.5),
        ),
        ModelVariant(
            "logistic_current",
            "model_family",
            "Regularized logistic regression with median imputation and scaling.",
            baseline,
            _logistic_regression,
        ),
        ModelVariant(
            "xgboost_no_recent_form",
            "feature_ablation",
            "Current XGBoost without recent-form features.",
            _without(baseline, RECENT_FORM_FEATURES),
            _xgboost,
        ),
        ModelVariant(
            "xgboost_no_damage",
            "feature_ablation",
            "Current XGBoost without damage proxy features.",
            _without(baseline, DAMAGE_FEATURES),
            _xgboost,
        ),
        ModelVariant(
            "xgboost_no_common_opponents",
            "feature_ablation",
            "Current XGBoost without common-opponent features.",
            _without(baseline, COMMON_OPPONENT_FEATURES),
            _xgboost,
        ),
        ModelVariant(
            "xgboost_no_stance",
            "feature_ablation",
            "Current XGBoost without stance interaction features.",
            _without(baseline, STANCE_FEATURES),
            _xgboost,
        ),
    ]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Market-Aware Model-Family Experiments",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Scored events: {report['coverage']['scored_events']}",
        f"- Scored fights: {report['coverage']['scored_fights']}",
        f"- Model-eligible events: {report['coverage']['model_eligible_events']}",
        f"- Model-eligible fights: {report['coverage']['model_eligible_fights']}",
        "",
        "## Gate",
        "",
        f"- Market favorite ROI: {_fmt_pct(report['market_baseline']['roi_pct'])}",
        f"- Best candidate: `{report['gate']['best_candidate']}`",
        f"- Best candidate ROI: {_fmt_pct(report['gate']['best_candidate_roi_pct'])}",
        f"- Delta vs market favorite: {_fmt_signed_pct(report['gate']['best_candidate_roi_delta_vs_market_favorite'])}",
        f"- Candidate cleared +2pp gate: `{str(report['gate']['candidate_cleared_gate']).lower()}`",
        f"- Rejection reasons: {', '.join(report['gate']['best_candidate_rejection_reasons']) or 'none'}",
        "",
        "## Variants",
        "",
        "| Variant | Family | Events | Fights | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate | Rejection reasons |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for variant in report["variants"]:
        metrics = variant["metrics"]
        roi = variant["simulated_research_roi"]
        lines.append(
            "| {name} | {family} | {events} | {count} | {accuracy} | {log_loss} | {brier} | {roi} | {delta} | {clears} | {reasons} |".format(
                name=variant["name"],
                family=variant["family"],
                events=variant["events_scored"],
                count=metrics["count"],
                accuracy=_fmt_pct(metrics["accuracy"]),
                log_loss=_fmt_metric(metrics["log_loss"]),
                brier=_fmt_metric(metrics["brier_score"]),
                roi=_fmt_pct(roi["roi_pct"]),
                delta=_fmt_signed_pct(variant["roi_delta_vs_market_favorite"]),
                clears=str(variant["clears_market_roi_gate"]).lower(),
                reasons=", ".join(variant["rejection_reasons"]) or "",
            )
        )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            report["value_status_reason"],
            "This experiment does not save model files, write `model_versions`, or activate value claims.",
        ]
    )
    return "\n".join(lines)


def _evaluate_model_variants(
    variants: list[ModelVariant],
    *,
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    min_train_samples: int,
) -> list[dict[str, Any]]:
    return [
        _evaluate_model_variant(
            variant,
            training_samples=training_samples,
            evaluation_samples=evaluation_samples,
            markets=markets,
            min_train_samples=min_train_samples,
        )
        for variant in variants
    ]


def _evaluate_model_variant(
    variant: ModelVariant,
    *,
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    min_train_samples: int,
) -> dict[str, Any]:
    predictions: list[dict[str, Any]] = []
    events = _evaluation_events(evaluation_samples)
    print(f"scoring {variant.name} across {len(events)} market-covered events", file=sys.stderr, flush=True)
    for event in events:
        train_samples = [sample for sample in training_samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in evaluation_samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
            continue
        model = variant.model_factory()
        train_x = _project_matrix(train_samples, variant.feature_names)
        train_y = np.array([sample["label"] for sample in train_samples], dtype=int)
        model.fit(train_x, train_y)
        target_x = _project_matrix(target_samples, variant.feature_names)
        probabilities = model.predict_proba(target_x)[:, 1]
        predictions.extend(
            _prediction_row(sample, probability, markets, variant.probability_fn)
            for sample, probability in zip(target_samples, probabilities, strict=True)
        )
    return _variant_report(variant, predictions)


def _evaluate_market_favorite(
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    predictions = []
    for sample in samples:
        market = markets[sample["fight_id"]]
        probability = market[sample["fighter_a_id"]]["market_prob"]
        predictions.append(_prediction_row(sample, probability, markets, None))
    return {
        "name": "market_favorite",
        "family": "market_baseline",
        "description": "No-vig market favorite baseline.",
        "feature_count": 0,
        "events_scored": len({sample["event_id"] for sample in samples}),
        "metrics": _metrics(predictions),
        "by_confidence_bucket": _grouped_market_metrics(predictions, lambda row: _confidence_bucket(row["confidence"])),
        "simulated_research_roi": _roi(predictions),
    }


def _variant_report(variant: ModelVariant, predictions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": variant.name,
        "family": variant.family,
        "description": variant.description,
        "feature_count": len(variant.feature_names),
        "feature_names": variant.feature_names,
        "events_scored": len({prediction["event_id"] for prediction in predictions}),
        "metrics": _metrics(predictions),
        "by_confidence_bucket": _grouped_market_metrics(predictions, lambda row: _confidence_bucket(row["confidence"])),
        "simulated_research_roi": _roi(predictions),
    }


def _prediction_row(
    sample: dict[str, Any],
    model_probability: float,
    markets: dict[str, dict[str, dict[str, float]]],
    probability_fn: ProbabilityFn | None,
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    market_probability = market[sample["fighter_a_id"]]["market_prob"]
    fighter_a_probability = probability_fn(model_probability, market_probability) if probability_fn else model_probability
    predicted_label = 1 if fighter_a_probability >= 0.5 else 0
    picked_fighter_id = sample["fighter_a_id"] if predicted_label == 1 else sample["fighter_b_id"]
    pick_market = market[picked_fighter_id]
    won = predicted_label == sample["label"]
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "fighter_a_probability": float(fighter_a_probability),
        "actual_label": sample["label"],
        "predicted_label": predicted_label,
        "confidence": float(fighter_a_probability if predicted_label == 1 else 1 - fighter_a_probability),
        "won": won,
        "decimal_odds": pick_market["decimal_odds"],
        "net_profit": flat_stake_net_profit(pick_market["decimal_odds"], won),
    }


def _grouped_market_metrics(
    predictions: list[dict[str, Any]],
    key_fn: Callable[[dict[str, Any]], str],
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in predictions:
        grouped.setdefault(key_fn(row), []).append(row)
    return {key: _metrics(rows) for key, rows in sorted(grouped.items())}


def _annotate_candidate(
    report: dict[str, Any],
    market_roi: float | None,
    market_metrics: dict[str, Any],
) -> None:
    roi = report["simulated_research_roi"]["roi_pct"]
    report["roi_delta_vs_market_favorite"] = roi_delta(roi, market_roi)
    reasons = _rejection_reasons(report, market_metrics)
    report["rejection_reasons"] = reasons
    report["clears_market_roi_gate"] = not reasons


def _rejection_reasons(report: dict[str, Any], market_metrics: dict[str, Any]) -> list[str]:
    if report["name"] == "market_favorite":
        return ["baseline_not_candidate"]
    reasons = []
    delta = report["roi_delta_vs_market_favorite"]
    if delta is None or delta < MIN_MARKET_ROI_DELTA:
        reasons.append("roi_delta_below_plus_2pp_market_gate")
    if report["metrics"]["count"] < 200 or report["events_scored"] < 30:
        reasons.append("unstable_coverage_bucket")
    if _metric_worse(report["metrics"].get("log_loss"), market_metrics.get("log_loss")):
        reasons.append("log_loss_worse_than_market")
    if _metric_worse(report["metrics"].get("brier_score"), market_metrics.get("brier_score")):
        reasons.append("brier_worse_than_market")
    if _metric_worse(report["metrics"].get("abs_calibration_error"), market_metrics.get("abs_calibration_error")):
        reasons.append("calibration_worse_than_market")
    return reasons


def _metric_worse(value: Any, baseline: Any) -> bool:
    return value is not None and baseline is not None and float(value) > float(baseline)


def _eligible_evaluation_samples(
    samples: list[dict[str, Any]],
    min_train_samples: int,
) -> list[dict[str, Any]]:
    eligible = []
    for event in _evaluation_events(samples):
        prior_count = sum(1 for sample in samples if sample["event_date"] < event["event_date"])
        if prior_count < min_train_samples:
            continue
        eligible.extend(sample for sample in samples if sample["event_id"] == event["event_id"])
    return eligible


def _evaluation_events(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events_by_id = {}
    for sample in samples:
        events_by_id[sample["event_id"]] = {
            "event_id": sample["event_id"],
            "event_date": sample["event_date"],
        }
    return sorted(events_by_id.values(), key=lambda row: (row["event_date"], row["event_id"]))


def _project_matrix(samples: list[dict[str, Any]], feature_names: list[str]) -> np.ndarray:
    index_by_name = {name: index for index, name in enumerate(FEATURE_NAMES)}
    indices = [index_by_name[name] for name in feature_names]
    return np.vstack([sample["features"][indices] for sample in samples])


def _without(feature_names: list[str], excluded: set[str]) -> list[str]:
    return [name for name in feature_names if name not in excluded]


def _xgboost() -> XGBClassifier:
    return XGBClassifier(
        n_estimators=40,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        n_jobs=1,
        random_state=42,
    )


def _logistic_regression() -> Any:
    return make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=42),
    )


def _fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _fmt_signed_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:+.1f}pp"


def _fmt_metric(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run report-only market-aware model-family experiments")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--min-train-samples", type=int, default=MIN_TRAIN_SAMPLES)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_model_family_experiments(
        output_path=output_path,
        markdown_path=markdown_path,
        min_train_samples=args.min_train_samples,
    )
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "gate": report["gate"],
        "market_baseline": report["market_baseline"],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
