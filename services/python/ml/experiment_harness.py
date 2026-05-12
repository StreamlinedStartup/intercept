"""Config-driven report-only market experiment harness."""
from __future__ import annotations

import argparse
import json
import subprocess
import warnings
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from ml.baselines import _load_market_consensus
from ml.features import (
    FEATURE_NAMES,
    OPPONENT_ADJUSTED_RECENT_PERFORMANCE_FEATURE_NAMES,
    build_opponent_adjusted_recent_performance_features,
)
from ml.market_blend_experiments import blend_probability, roi_delta
from ml.market_gate_report import (
    _fmt_metric,
    _fmt_pct,
    _fmt_signed_pct,
    _load_matched_market_samples,
    _metrics,
    _resolve_repo_path,
    _roi,
)
from ml.market_residual_analysis import _prediction_fields
from ml.market_signal_experiment import (
    AVAILABILITY_FEATURE_NAMES,
    _availability_augmented_features,
    _base_features,
)
from ml.model_family_experiments import (
    COMMON_OPPONENT_FEATURES,
    DAMAGE_FEATURES,
    RECENT_FORM_FEATURES,
    STANCE_FEATURES,
    _eligible_evaluation_samples,
    _evaluation_events,
)
from ml.odds_aware_report import _load_source_coverage
from ml.train import REPO_ROOT

DEFAULT_CONFIG = REPO_ROOT / "configs" / "experiments" / "market-grid.example.json"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "harness" / "market-grid-smoke.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "harness" / "market-grid-smoke.md"

type FeatureFn = Callable[[dict[str, Any]], np.ndarray]

FEATURE_GROUPS = {
    "common_opponents": COMMON_OPPONENT_FEATURES,
    "damage": DAMAGE_FEATURES,
    "recent_form": RECENT_FORM_FEATURES,
    "stance": STANCE_FEATURES,
}
XGBOOST_PARAM_DEFAULTS = {
    "n_estimators": 40,
    "max_depth": 3,
    "learning_rate": 0.05,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
}
XGBOOST_PARAM_KEYS = set(XGBOOST_PARAM_DEFAULTS)
LOGISTIC_PARAM_KEYS = {"C"}


def run_experiment_harness(
    *,
    config_path: Path = DEFAULT_CONFIG,
    output_path: Path | None = None,
    markdown_path: Path | None = None,
) -> dict[str, Any]:
    config = _load_config(config_path)
    output_path = output_path or _resolve_repo_path(Path(config["outputs"]["json"]))
    markdown_path = markdown_path or _resolve_repo_path(Path(config["outputs"]["markdown"]))
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    max_events = config["corpus"].get("max_events")
    if max_events is not None:
        keep_events = {event["event_id"] for event in _evaluation_events(samples)[: int(max_events)]}
        samples = [sample for sample in samples if sample["event_id"] in keep_events]
    min_train_samples = int(config["corpus"]["min_train_samples"])
    eligible_samples = _eligible_evaluation_samples(samples, min_train_samples)
    markets = _load_market_consensus()
    market_predictions = [_market_prediction(sample, markets) for sample in eligible_samples]
    base_prediction_cache: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    market_report = _variant_report(
        {
            "name": "market_favorite",
            "model": "market_favorite",
            "features": "none",
            "market_blend_weight": None,
            "description": "No-vig market favorite baseline.",
        },
        market_predictions,
    )
    reports = []
    for variant in config["variants"]:
        if variant["name"] == "market_favorite" or variant["model"] == "market_favorite":
            report = market_report
        else:
            report = _run_model_variant(
                variant,
                samples,
                eligible_samples,
                markets,
                min_train_samples,
                base_prediction_cache,
            )
        _annotate_variant(report, market_report, config["gate"])
        reports.append(report)
    if not any(report["name"] == "market_favorite" for report in reports):
        _annotate_variant(market_report, market_report, config["gate"])
        reports.insert(0, market_report)
    ranked = sorted(reports, key=_ranking_key)
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-experiment-harness",
        "config_path": _display_path(config_path),
        "git_sha": _git_sha(),
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "config": config,
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
            "model_eligible_events": len({sample["event_id"] for sample in eligible_samples}),
            "model_eligible_fights": len(eligible_samples),
        },
        "market_baseline": {
            "name": market_report["name"],
            "roi_pct": market_report["simulated_research_roi"]["roi_pct"],
            "accuracy": market_report["metrics"]["accuracy"],
            "log_loss": market_report["metrics"]["log_loss"],
            "brier_score": market_report["metrics"]["brier_score"],
        },
        "variants": reports,
        "ranking": [
            {
                "rank": index,
                "name": variant["name"],
                "roi_delta_vs_market": variant["roi_delta_vs_market"],
                "log_loss_delta_vs_market": variant["log_loss_delta_vs_market"],
                "brier_delta_vs_market": variant["brier_delta_vs_market"],
                "clears_gate": variant["clears_market_gate"],
                "rejection_reasons": variant["rejection_reasons"],
            }
            for index, variant in enumerate(ranked, start=1)
        ],
        "recommendation": _recommendation(ranked),
        "policy": (
            "This harness is for report-only discovery. A candidate from the current corpus is not activation proof; "
            "validated status requires a locked future evaluation slice and a passing market gate."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Market Experiment Harness",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Config: `{report['config_path']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Model-eligible events: {report['coverage']['model_eligible_events']}",
        f"- Model-eligible fights: {report['coverage']['model_eligible_fights']}",
        "",
        "## Ranking",
        "",
        "| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |",
        "|---:|---|---:|---:|---:|---|---|",
    ]
    for row in report["ranking"]:
        lines.append(
            "| {rank} | {name} | {roi_delta} | {log_loss_delta} | {brier_delta} | {clears} | {reasons} |".format(
                rank=row["rank"],
                name=row["name"],
                roi_delta=_fmt_signed_pct(row["roi_delta_vs_market"]),
                log_loss_delta=_fmt_metric(row["log_loss_delta_vs_market"]),
                brier_delta=_fmt_metric(row["brier_delta_vs_market"]),
                clears=str(row["clears_gate"]).lower(),
                reasons=", ".join(row["rejection_reasons"]) or "",
            )
        )
    lines.extend(
        [
            "",
            "## Variants",
            "",
            "| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for variant in report["variants"]:
        metrics = variant["metrics"]
        roi = variant["simulated_research_roi"]
        lines.append(
            "| {name} | {model} | {features} | {weight} | {count} | {accuracy} | {log_loss} | {brier} | {roi} |".format(
                name=variant["name"],
                model=variant["params"]["model"],
                features=variant["params"]["features"],
                weight="" if variant["params"]["market_blend_weight"] is None else variant["params"]["market_blend_weight"],
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


def _load_config(path: Path) -> dict[str, Any]:
    resolved = _resolve_repo_path(path)
    config = json.loads(resolved.read_text())
    _validate_config(config)
    return config


def _validate_config(config: dict[str, Any]) -> None:
    required = {"name", "description", "corpus", "split", "gate", "variants", "outputs"}
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"experiment config missing required keys: {', '.join(missing)}")
    if config.get("value_status") != "research_only":
        raise ValueError("experiment config must keep value_status='research_only'")
    if config.get("report_only") is not True:
        raise ValueError("experiment config must set report_only=true")
    if config.get("writes_model_versions") is not False:
        raise ValueError("experiment config must set writes_model_versions=false")
    if config["split"]["policy"] != "chronological_walk_forward":
        raise ValueError("only chronological_walk_forward split is supported")
    if config["gate"]["baseline"] != "market_favorite":
        raise ValueError("only market_favorite gate baseline is supported")
    names = [variant["name"] for variant in config["variants"]]
    if len(names) != len(set(names)):
        raise ValueError("variant names must be unique")
    for variant in config["variants"]:
        if variant["model"] == "market_favorite" and variant["features"] != "none":
            raise ValueError("market_favorite variant must use features='none'")
        if variant.get("market_blend_weight") is not None and variant["model"] == "market_favorite":
            raise ValueError("market_favorite variant cannot set market_blend_weight")
        _validate_model_params(variant)
        _feature_spec(variant)
        _feature_names(variant)
        _calibration(variant)


def _run_model_variant(
    variant: dict[str, Any],
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    min_train_samples: int,
    base_prediction_cache: dict[tuple[Any, ...], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    cache = base_prediction_cache if base_prediction_cache is not None else {}
    key = _base_prediction_key(variant, min_train_samples)
    if key not in cache:
        cache[key] = _score_base_walk_forward(variant, training_samples, evaluation_samples, min_train_samples)
    predictions = _materialize_predictions(cache[key], markets, _calibration(variant), variant.get("market_blend_weight"))
    return _variant_report(variant, predictions)


def _score_base_walk_forward(
    variant: dict[str, Any],
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    min_train_samples: int,
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    feature_fn = _feature_fn(variant)
    for event in _evaluation_events(evaluation_samples):
        train_samples = [sample for sample in training_samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in evaluation_samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
            continue
        model = _model(variant["model"], _model_params(variant))
        train_x = np.vstack([feature_fn(sample) for sample in train_samples])
        train_y = np.array([sample["label"] for sample in train_samples], dtype=int)
        model.fit(train_x, train_y)
        target_x = np.vstack([feature_fn(sample) for sample in target_samples])
        probabilities = model.predict_proba(target_x)[:, 1]
        predictions.extend(
            {"sample": sample, "model_probability": float(probability)}
            for sample, probability in zip(target_samples, probabilities, strict=True)
        )
    return predictions


def _materialize_predictions(
    base_predictions: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    calibration: dict[str, Any],
    market_blend_weight: float | None,
) -> list[dict[str, Any]]:
    return [
        _prediction(
            base_prediction["sample"],
            markets,
            _calibrate_probability(float(base_prediction["model_probability"]), calibration),
            market_blend_weight,
        )
        for base_prediction in base_predictions
    ]


def _market_prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    probability = market[sample["fighter_a_id"]]["market_prob"]
    return _prediction(sample, markets, probability, None)


def _prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    model_probability: float,
    market_blend_weight: float | None,
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    market_probability = market[sample["fighter_a_id"]]["market_prob"]
    probability = (
        blend_probability(model_probability, market_probability, float(market_blend_weight))
        if market_blend_weight is not None
        else model_probability
    )
    prediction = _prediction_fields(sample, market, probability)
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "fighter_a_probability": prediction["fighter_a_probability"],
        "actual_label": sample["label"],
        "predicted_label": prediction["predicted_label"],
        "confidence": prediction["confidence"],
        "won": prediction["won"],
        "decimal_odds": prediction["decimal_odds"],
        "net_profit": prediction["net_profit"],
    }


def _variant_report(variant: dict[str, Any], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": variant["name"],
        "description": variant.get("description", ""),
        "params": {
            "model": variant["model"],
            "features": variant["features"],
            "feature_names": _feature_names(variant),
            "market_blend_weight": variant.get("market_blend_weight"),
            "model_params": _model_params(variant),
            "calibration": _calibration(variant),
            "feature_count": _feature_count(variant),
        },
        "events_scored": len({prediction["event_id"] for prediction in predictions}),
        "metrics": _safe_metrics(predictions),
        "simulated_research_roi": _roi(predictions),
    }


def _annotate_variant(report: dict[str, Any], market: dict[str, Any], gate: dict[str, Any]) -> None:
    report["roi_delta_vs_market"] = roi_delta(
        report["simulated_research_roi"]["roi_pct"],
        market["simulated_research_roi"]["roi_pct"],
    )
    report["log_loss_delta_vs_market"] = _delta(report["metrics"]["log_loss"], market["metrics"]["log_loss"])
    report["brier_delta_vs_market"] = _delta(report["metrics"]["brier_score"], market["metrics"]["brier_score"])
    reasons = _rejection_reasons(report, gate)
    report["rejection_reasons"] = reasons
    report["clears_market_gate"] = not reasons


def _rejection_reasons(report: dict[str, Any], gate: dict[str, Any]) -> list[str]:
    if report["name"] == "market_favorite":
        return ["baseline_not_candidate"]
    reasons = []
    min_delta = float(gate["min_roi_delta_vs_market"])
    if report["roi_delta_vs_market"] is None or report["roi_delta_vs_market"] < min_delta:
        reasons.append("roi_delta_below_market_gate")
    quality = gate["probability_quality"]
    if quality["require_log_loss_not_worse"] and _positive(report["log_loss_delta_vs_market"]):
        reasons.append("log_loss_worse_than_market")
    if quality["require_brier_not_worse"] and _positive(report["brier_delta_vs_market"]):
        reasons.append("brier_worse_than_market")
    if report["metrics"]["count"] < 200 or report["events_scored"] < 30:
        reasons.append("unstable_coverage")
    return reasons


def _recommendation(ranked: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = [row for row in ranked if row["name"] != "market_favorite"]
    best = candidates[0] if candidates else None
    if best is None:
        return {"status": "no_candidates", "reason": "No non-market variants were configured."}
    if best["clears_market_gate"]:
        return {
            "status": "candidate_for_locked_evaluation",
            "reason": f"{best['name']} clears the configured discovery gate; evaluate on a locked future slice before activation.",
        }
    return {
        "status": "research_only",
        "reason": f"{best['name']} is the best configured candidate but does not clear the market gate.",
    }


def _ranking_key(report: dict[str, Any]) -> tuple[int, float, float, float, str]:
    if report["name"] == "market_favorite":
        return (1, 0, 0, 0, report["name"])
    roi_delta_value = report["roi_delta_vs_market"]
    log_loss_delta = report["log_loss_delta_vs_market"]
    brier_delta = report["brier_delta_vs_market"]
    return (
        0,
        -(roi_delta_value if roi_delta_value is not None else float("-inf")),
        log_loss_delta if log_loss_delta is not None else float("inf"),
        brier_delta if brier_delta is not None else float("inf"),
        report["name"],
    )


def _base_prediction_key(variant: dict[str, Any], min_train_samples: int) -> tuple[Any, ...]:
    return (
        variant["model"],
        _stable_items(_model_params(variant)),
        tuple(_feature_names(variant)),
        min_train_samples,
    )


def _model(name: str, params: dict[str, Any] | None = None) -> Any:
    params = params or {}
    if name == "xgboost":
        return XGBClassifier(
            **{**XGBOOST_PARAM_DEFAULTS, **params},
            eval_metric="logloss",
            n_jobs=1,
            random_state=42,
        )
    if name == "logistic_regression":
        return make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=42, C=float(params.get("C", 1.0))),
        )
    raise ValueError(f"unsupported model {name!r}")


def _feature_fn(variant: dict[str, Any]) -> FeatureFn:
    names = _feature_names(variant)
    spec = _feature_spec(variant)
    base_names = _base_feature_names(spec["base"])
    base_fn = _base_feature_fn(spec["base"])
    if names == base_names:
        return base_fn
    index_by_name = {name: index for index, name in enumerate(base_names)}
    indices = [index_by_name[name] for name in names]

    def project(sample: dict[str, Any]) -> np.ndarray:
        return base_fn(sample)[indices]

    return project


def _feature_count(features: Any) -> int:
    if features == "none":
        return 0
    variant = {"model": "xgboost", "features": features} if not isinstance(features, dict) or "features" not in features else features
    return len(_feature_names(variant))


def _feature_names(variant: dict[str, Any]) -> list[str]:
    spec = _feature_spec(variant)
    if spec["base"] == "none":
        return []
    base = _base_feature_names(spec["base"])
    subset = variant.get("feature_subset")
    if subset is None:
        return base
    names = _resolve_feature_names(subset["names"], base)
    if subset["mode"] == "only":
        return names
    excluded = set(names)
    return [name for name in base if name not in excluded]


def _feature_spec(variant: dict[str, Any]) -> dict[str, Any]:
    features = variant["features"]
    if features == "none":
        if variant["model"] == "market_favorite":
            return {"base": "none"}
        raise ValueError("non-market variants cannot use features='none'")
    if features in {
        "production",
        "production_plus_availability",
        "production_plus_opponent_adjusted_recent_performance",
    }:
        return {"base": features}
    raise ValueError(f"unsupported feature set {features!r}")


def _base_feature_names(features: str) -> list[str]:
    if features == "production":
        return list(FEATURE_NAMES)
    if features == "production_plus_availability":
        return [*FEATURE_NAMES, *AVAILABILITY_FEATURE_NAMES]
    if features == "production_plus_opponent_adjusted_recent_performance":
        return [*FEATURE_NAMES, *OPPONENT_ADJUSTED_RECENT_PERFORMANCE_FEATURE_NAMES]
    raise ValueError(f"unsupported feature set {features!r}")


def _base_feature_fn(features: str) -> FeatureFn:
    if features == "production":
        return _base_features
    if features == "production_plus_availability":
        return _availability_augmented_features
    if features == "production_plus_opponent_adjusted_recent_performance":
        return _opponent_adjusted_recent_performance_features
    raise ValueError(f"unsupported feature set {features!r}")


def _opponent_adjusted_recent_performance_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate(
        [
            sample["features"],
            build_opponent_adjusted_recent_performance_features(
                sample["fighter_a_id"],
                sample["fighter_b_id"],
                sample["event_date"],
            ),
        ]
    )


def _resolve_feature_names(names: list[str], base: list[str]) -> list[str]:
    resolved: list[str] = []
    for name in names:
        if name in FEATURE_GROUPS:
            resolved.extend(feature for feature in base if feature in FEATURE_GROUPS[name])
        elif name in base:
            resolved.append(name)
        else:
            raise ValueError(f"unknown feature or group {name!r}")
    unique: list[str] = []
    for name in resolved:
        if name not in unique:
            unique.append(name)
    if not unique:
        raise ValueError("feature_subset resolved to no features")
    return unique


def _model_params(variant: dict[str, Any]) -> dict[str, Any]:
    return dict(variant.get("model_params") or {})


def _validate_model_params(variant: dict[str, Any]) -> None:
    params = _model_params(variant)
    if not params:
        return
    if variant["model"] == "xgboost":
        unsupported = sorted(set(params) - XGBOOST_PARAM_KEYS)
    elif variant["model"] == "logistic_regression":
        unsupported = sorted(set(params) - LOGISTIC_PARAM_KEYS)
    else:
        unsupported = sorted(params)
    if unsupported:
        raise ValueError(f"unsupported model_params for {variant['model']}: {', '.join(unsupported)}")


def _calibration(variant: dict[str, Any]) -> dict[str, Any]:
    calibration = dict(variant.get("calibration") or {"method": "none"})
    if calibration["method"] == "none":
        return {"method": "none"}
    if calibration["method"] == "temperature":
        return {"method": "temperature", "temperature": float(calibration["temperature"])}
    raise ValueError(f"unsupported calibration method {calibration['method']!r}")


def _calibrate_probability(probability: float, calibration: dict[str, Any]) -> float:
    if calibration["method"] == "none":
        return float(np.clip(probability, 0.001, 0.999))
    if calibration["method"] == "temperature":
        temperature = float(calibration["temperature"])
        clipped = float(np.clip(probability, 1e-6, 1 - 1e-6))
        logit = np.log(clipped / (1 - clipped))
        return float(np.clip(1 / (1 + np.exp(-(logit / temperature))), 0.001, 0.999))
    raise ValueError(f"unsupported calibration method {calibration['method']!r}")


def _stable_items(values: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
    return tuple(sorted(values.items()))


def _safe_metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        return _metrics(predictions)


def _positive(value: float | None) -> bool:
    return value is not None and value > 0


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def _git_sha() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _display_path(path: Path) -> str:
    resolved = _resolve_repo_path(path)
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run config-driven market experiment harness")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--markdown", type=Path, default=None)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output) if args.output is not None else None
    markdown_path = _resolve_repo_path(args.markdown) if args.markdown is not None else None
    report = run_experiment_harness(
        config_path=args.config,
        output_path=output_path,
        markdown_path=markdown_path,
    )
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": report["config"]["outputs"]["json"] if output_path is None else _display_path(output_path),
        "markdown": report["config"]["outputs"]["markdown"] if markdown_path is None else _display_path(markdown_path),
        "coverage": report["coverage"],
        "recommendation": report["recommendation"],
        "top_ranked": report["ranking"][:5],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
