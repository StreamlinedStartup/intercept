"""Config-driven report-only market experiment harness."""
from __future__ import annotations

import argparse
import json
import subprocess
import warnings
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np
from psycopg.rows import dict_row
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from ml.baselines import _load_market_consensus
from ml.db import pool
from ml.features import (
    FEATURE_NAMES,
    OPPONENT_ADJUSTED_RECENT_PERFORMANCE_FEATURE_NAMES,
    STYLE_MATCHUP_PRESSURE_FEATURE_NAMES,
    build_opponent_adjusted_recent_performance_features,
    build_style_matchup_pressure_features,
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
MARKET_CONTEXT_FEATURE_NAMES = [
    "fighter_a_market_probability",
    "fighter_b_market_probability",
    "market_probability_edge",
    "market_uncertainty",
]
XGBOOST_PARAM_DEFAULTS = {
    "n_estimators": 40,
    "max_depth": 3,
    "learning_rate": 0.05,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
}
XGBOOST_PARAM_KEYS = set(XGBOOST_PARAM_DEFAULTS)
LOGISTIC_PARAM_KEYS = {"C"}
SUPPORTED_TARGETS = {"winner", "decision", "finish"}


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
    samples = _attach_target_labels(samples)
    max_events = config["corpus"].get("max_events")
    if max_events is not None:
        keep_events = {event["event_id"] for event in _evaluation_events(samples)[: int(max_events)]}
        samples = [sample for sample in samples if sample["event_id"] in keep_events]
    min_train_samples = int(config["corpus"]["min_train_samples"])
    eligible_samples = _eligible_evaluation_samples(samples, min_train_samples)
    eligible_samples = _apply_holdout_policy(eligible_samples, config["corpus"].get("holdout"))
    markets = _load_market_consensus()
    prop_markets = _load_prop_market_consensus()
    samples = _attach_market_context(samples, markets)
    eligible_samples = _attach_market_context(eligible_samples, markets)
    market_predictions = [_market_prediction(sample, markets) for sample in eligible_samples]
    base_prediction_cache: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    feature_vector_cache: dict[tuple[tuple[str, ...], str], np.ndarray] = {}
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
    target_market_reports = {
        "winner": market_report,
        "decision": _target_market_baseline_report("decision", eligible_samples, prop_markets),
        "finish": _target_market_baseline_report("finish", eligible_samples, prop_markets),
    }
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
                prop_markets,
                min_train_samples,
                base_prediction_cache,
                feature_vector_cache,
            )
        _annotate_variant(report, report.get("gate_baseline", target_market_reports[_target(variant)]), config["gate"])
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
            "holdout": _holdout_summary(config["corpus"].get("holdout"), eligible_samples),
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
            "| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for variant in report["variants"]:
        metrics = variant["metrics"]
        roi = variant["simulated_research_roi"]
        lines.append(
            "| {name} | {target} | {model} | {features} | {weight} | {count} | {accuracy} | {log_loss} | {brier} | {roi} |".format(
                name=variant["name"],
                target=variant["params"]["target"],
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
        _target(variant)
        if variant.get("market_blend_weight") is not None and _target(variant) != "winner":
            raise ValueError("market_blend_weight requires target='winner'")
        _validate_model_params(variant)
        _feature_spec(variant)
        _feature_names(variant)
        _calibration(variant)
        _selection_policy(variant)
    _holdout_policy(config["corpus"].get("holdout"))


def _holdout_policy(policy: dict[str, Any] | None) -> dict[str, Any] | None:
    if policy is None:
        return None
    policy_type = policy.get("type")
    if policy_type == "last_n_events":
        event_count = int(policy.get("event_count", 0))
        if event_count < 1:
            raise ValueError("holdout last_n_events requires event_count >= 1")
        return {"type": "last_n_events", "event_count": event_count}
    if policy_type == "after_date":
        value = policy.get("after_date")
        if not isinstance(value, str):
            raise ValueError("holdout after_date requires after_date")
        return {"type": "after_date", "after_date": date.fromisoformat(value)}
    raise ValueError(f"unsupported holdout policy {policy_type!r}")


def _apply_holdout_policy(
    eligible_samples: list[dict[str, Any]],
    policy: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    normalized = _holdout_policy(policy)
    if normalized is None:
        return eligible_samples
    events = _evaluation_events(eligible_samples)
    if normalized["type"] == "last_n_events":
        keep_events = {event["event_id"] for event in events[-int(normalized["event_count"]) :]}
    else:
        keep_events = {
            event["event_id"]
            for event in events
            if event["event_date"] > normalized["after_date"]
        }
    return [sample for sample in eligible_samples if sample["event_id"] in keep_events]


def _holdout_summary(policy: dict[str, Any] | None, eligible_samples: list[dict[str, Any]]) -> dict[str, Any] | None:
    normalized = _holdout_policy(policy)
    if normalized is None:
        return None
    events = _evaluation_events(eligible_samples)
    summary = {
        "events": len(events),
        "fights": len(eligible_samples),
        "start_date": events[0]["event_date"].isoformat() if events else None,
        "end_date": events[-1]["event_date"].isoformat() if events else None,
    }
    if normalized["type"] == "after_date":
        return {**summary, "type": "after_date", "after_date": normalized["after_date"].isoformat()}
    return {
        **normalized,
        **summary,
    }


def _run_model_variant(
    variant: dict[str, Any],
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    prop_markets: dict[str, dict[str, dict[str, float]]],
    min_train_samples: int,
    base_prediction_cache: dict[tuple[Any, ...], list[dict[str, Any]]] | None = None,
    feature_vector_cache: dict[tuple[tuple[str, ...], str], np.ndarray] | None = None,
) -> dict[str, Any]:
    cache = base_prediction_cache if base_prediction_cache is not None else {}
    key = _base_prediction_key(variant, min_train_samples)
    if key not in cache:
        cache[key] = _score_base_walk_forward(
            variant,
            training_samples,
            evaluation_samples,
            min_train_samples,
            feature_vector_cache,
        )
    predictions = _materialize_predictions(
        cache[key],
        markets,
        prop_markets,
        _calibration(variant),
        variant.get("market_blend_weight"),
        _target(variant),
    )
    selected_predictions = _apply_selection_policy(predictions, _selection_policy(variant))
    report = _variant_report(variant, selected_predictions)
    if _selection_policy(variant)["type"] != "all":
        selected_ids = {prediction["fight_id"] for prediction in selected_predictions}
        selected_samples = [
            base_prediction["sample"] for base_prediction in cache[key] if base_prediction["sample"]["fight_id"] in selected_ids
        ]
        report["gate_baseline"] = _variant_report(
            {
                "name": f"{variant['name']}_market_selected_baseline",
                "model": "market_favorite" if _target(variant) == "winner" else "prop_market_baseline",
                "target": _target(variant),
                "features": "none",
                "market_blend_weight": None,
                "description": "No-vig market baseline on the selected fight subset.",
            },
            _target_market_predictions(_target(variant), selected_samples, markets, prop_markets),
        )
    return report


def _score_base_walk_forward(
    variant: dict[str, Any],
    training_samples: list[dict[str, Any]],
    evaluation_samples: list[dict[str, Any]],
    min_train_samples: int,
    feature_vector_cache: dict[tuple[tuple[str, ...], str], np.ndarray] | None = None,
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    target = _target(variant)
    feature_fn = _feature_fn(variant)
    feature_names = tuple(_feature_names(variant))
    cache = feature_vector_cache if feature_vector_cache is not None else {}
    for event in _evaluation_events(evaluation_samples):
        train_samples = [sample for sample in training_samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in evaluation_samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
            continue
        model = _model(variant["model"], _model_params(variant))
        train_labels = [_target_label(sample, target) for sample in train_samples]
        target_labels = [_target_label(sample, target) for sample in target_samples]
        train_pairs = [
            (sample, label)
            for sample, label in zip(train_samples, train_labels, strict=True)
            if label is not None
        ]
        target_pairs = [
            (sample, label)
            for sample, label in zip(target_samples, target_labels, strict=True)
            if label is not None
        ]
        if len(train_pairs) < min_train_samples or not target_pairs:
            continue
        train_y = np.array([label for _sample, label in train_pairs], dtype=int)
        if len(set(train_y.tolist())) < 2:
            continue
        train_x = np.vstack([_cached_feature_vector(sample, feature_names, feature_fn, cache) for sample, _label in train_pairs])
        model.fit(train_x, train_y)
        target_x = np.vstack([_cached_feature_vector(sample, feature_names, feature_fn, cache) for sample, _label in target_pairs])
        probabilities = model.predict_proba(target_x)[:, 1]
        predictions.extend(
            {"sample": sample, "model_probability": float(probability)}
            for (sample, _label), probability in zip(target_pairs, probabilities, strict=True)
        )
    return predictions


def _cached_feature_vector(
    sample: dict[str, Any],
    feature_names: tuple[str, ...],
    feature_fn: FeatureFn,
    cache: dict[tuple[tuple[str, ...], str], np.ndarray],
) -> np.ndarray:
    key = (feature_names, str(sample["fight_id"]))
    if key not in cache:
        cache[key] = feature_fn(sample)
    return cache[key]


def _materialize_predictions(
    base_predictions: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    prop_markets: dict[str, dict[str, dict[str, float]]] | None,
    calibration: dict[str, Any],
    market_blend_weight: float | None,
    target: str = "winner",
) -> list[dict[str, Any]]:
    return [
        _target_prediction(
            base_prediction["sample"],
            markets,
            prop_markets or {},
            _calibrate_probability(float(base_prediction["model_probability"]), calibration),
            market_blend_weight,
            target,
        )
        for base_prediction in base_predictions
    ]


def _apply_selection_policy(
    predictions: list[dict[str, Any]],
    policy: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if policy is None or policy["type"] == "all":
        return predictions
    policy_type = policy["type"]
    if policy_type == "market_favorite_only":
        return [prediction for prediction in predictions if prediction["picked_market_probability"] >= 0.5]
    if policy_type == "market_underdog_only":
        return [prediction for prediction in predictions if prediction["picked_market_probability"] < 0.5]
    if policy_type == "model_market_agree":
        return [prediction for prediction in predictions if prediction["predicted_label"] == prediction["market_predicted_label"]]
    if policy_type == "model_market_disagree":
        return [prediction for prediction in predictions if prediction["predicted_label"] != prediction["market_predicted_label"]]
    if policy_type == "min_confidence":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if prediction["confidence"] >= threshold]
    if policy_type == "min_model_market_edge":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if prediction["picked_model_market_edge"] >= threshold]
    if policy_type == "min_absolute_model_market_edge":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if abs(prediction["picked_model_market_edge"]) >= threshold]
    if policy_type == "overpriced_favorite":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if _overpriced_favorite_edge(prediction) >= threshold]
    if policy_type == "undervalued_underdog":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if _undervalued_underdog_edge(prediction) >= threshold]
    if policy_type == "decision_edge":
        threshold = float(policy["threshold"])
        return [
            prediction for prediction in predictions
            if prediction["target"] == "decision"
            and prediction["predicted_label"] == 1
            and prediction["picked_model_probability"] >= threshold
        ]
    if policy_type == "finish_edge":
        threshold = float(policy["threshold"])
        return [
            prediction for prediction in predictions
            if prediction["target"] == "finish"
            and prediction["predicted_label"] == 1
            and prediction["picked_model_probability"] >= threshold
        ]
    if policy_type == "abstain":
        threshold = float(policy["threshold"])
        return [prediction for prediction in predictions if prediction["confidence"] <= threshold]
    raise ValueError(f"unsupported selection policy {policy_type!r}")


def _selection_policy(variant: dict[str, Any]) -> dict[str, Any]:
    policy = dict(variant.get("selection_policy") or {"type": "all"})
    policy_type = policy.get("type")
    supported = {
        "all",
        "market_favorite_only",
        "market_underdog_only",
        "model_market_agree",
        "model_market_disagree",
        "min_confidence",
        "min_model_market_edge",
        "min_absolute_model_market_edge",
        "overpriced_favorite",
        "undervalued_underdog",
        "decision_edge",
        "finish_edge",
        "abstain",
    }
    if policy_type not in supported:
        raise ValueError(f"unsupported selection policy {policy_type!r}")
    threshold_policies = {
        "min_confidence",
        "min_model_market_edge",
        "min_absolute_model_market_edge",
        "overpriced_favorite",
        "undervalued_underdog",
        "decision_edge",
        "finish_edge",
        "abstain",
    }
    if policy_type in threshold_policies:
        if "threshold" not in policy:
            raise ValueError(f"selection policy {policy_type!r} requires threshold")
        policy["threshold"] = float(policy["threshold"])
    elif "threshold" in policy:
        raise ValueError(f"selection policy {policy_type!r} cannot set threshold")
    return policy


def _overpriced_favorite_edge(prediction: dict[str, Any]) -> float:
    if prediction["target"] != "winner" or prediction["market_predicted_label"] is None:
        return float("-inf")
    market_favorite_probability = (
        prediction["market_probability"]
        if prediction["market_predicted_label"] == 1
        else 1 - prediction["market_probability"]
    )
    model_favorite_probability = (
        prediction["fighter_a_probability"]
        if prediction["market_predicted_label"] == 1
        else 1 - prediction["fighter_a_probability"]
    )
    return float(market_favorite_probability - model_favorite_probability)


def _undervalued_underdog_edge(prediction: dict[str, Any]) -> float:
    if prediction["target"] != "winner" or prediction["market_predicted_label"] is None:
        return float("-inf")
    if prediction["predicted_label"] == prediction["market_predicted_label"]:
        return float("-inf")
    edge_value = prediction["picked_model_market_edge"]
    return float(edge_value) if edge_value is not None else float("-inf")


def _market_prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    probability = market[sample["fighter_a_id"]]["market_prob"]
    return _prediction(sample, markets, probability, None)


def _target_market_baseline_report(
    target: str,
    samples: list[dict[str, Any]],
    prop_markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    return _variant_report(
        {
            "name": f"{target}_market_baseline",
            "model": "prop_market_baseline",
            "target": target,
            "features": "none",
            "market_blend_weight": None,
            "description": f"No-vig FightOdds DISTANCE market baseline for {target}.",
        },
        _target_market_predictions(target, samples, {}, prop_markets),
    )


def _target_market_predictions(
    target: str,
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    prop_markets: dict[str, dict[str, dict[str, float]]],
) -> list[dict[str, Any]]:
    if target == "winner":
        return [_market_prediction(sample, markets) for sample in samples]
    predictions = []
    for sample in samples:
        probability = _prop_market_probability(prop_markets, str(sample["fight_id"]), target)
        if probability is not None and _target_label(sample, target) is not None:
            predictions.append(_target_prediction(sample, markets, prop_markets, probability, None, target))
    return predictions


def _load_prop_market_consensus() -> dict[str, dict[str, dict[str, float]]]:
    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    hof.canonical_fight_id AS fight_id,
                    hpo.source_market_id,
                    hpo.sportsbook_slug,
                    hpo.outcome_side,
                    hpo.implied_probability
                FROM historical_prop_odds hpo
                JOIN historical_odds_fights hof ON hof.id = hpo.historical_fight_id
                WHERE hpo.source_offer_type_id = 'DISTANCE'
                    AND hpo.market_family = 'fight_distance'
                    AND hpo.line_kind = 'source_current'
                    AND hof.canonical_fight_id IS NOT NULL
                """,
            )
            rows = cur.fetchall()
    return _prop_market_consensus_from_rows(rows)


def _prop_market_consensus_from_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, float]]]:
    pairs: dict[tuple[str, str, str], dict[str, float]] = {}
    for row in rows:
        key = (str(row["fight_id"]), str(row["source_market_id"]), str(row["sportsbook_slug"]))
        pairs.setdefault(key, {})[str(row["outcome_side"])] = float(row["implied_probability"])
    by_fight: dict[str, list[dict[str, float]]] = {}
    for (fight_id, _source_market_id, _sportsbook_slug), pair in pairs.items():
        probabilities = _novig_distance_probabilities(pair)
        if probabilities is not None:
            by_fight.setdefault(fight_id, []).append(probabilities)
    consensus: dict[str, dict[str, dict[str, float]]] = {}
    for fight_id, probabilities in by_fight.items():
        decision_probability = float(np.mean([row["decision"] for row in probabilities]))
        finish_probability = float(np.mean([row["finish"] for row in probabilities]))
        pair_count = len(probabilities)
        consensus[fight_id] = {
            "decision": {"market_prob": decision_probability, "pair_count": pair_count},
            "finish": {"market_prob": finish_probability, "pair_count": pair_count},
        }
    return consensus


def _novig_distance_probabilities(pair: dict[str, float]) -> dict[str, float] | None:
    decision_implied = pair.get("outcome1")
    finish_implied = pair.get("outcome2")
    if decision_implied is None or finish_implied is None:
        return None
    total = decision_implied + finish_implied
    if total <= 0:
        return None
    decision_probability = decision_implied / total
    return {
        "decision": decision_probability,
        "finish": 1 - decision_probability,
    }


def _prop_market_probability(
    prop_markets: dict[str, dict[str, dict[str, float]]],
    fight_id: str,
    target: str,
) -> float | None:
    if target not in {"decision", "finish"}:
        return None
    market = prop_markets.get(fight_id, {}).get(target)
    if market is None:
        return None
    return float(market["market_prob"])


def _target_prediction(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    prop_markets: dict[str, dict[str, dict[str, float]]],
    model_probability: float,
    market_blend_weight: float | None,
    target: str,
) -> dict[str, Any]:
    if target == "winner":
        return _prediction(sample, markets, model_probability, market_blend_weight)
    if market_blend_weight is not None:
        raise ValueError(f"market_blend_weight requires target='winner', got {target!r}")
    actual_label = _target_label(sample, target)
    if actual_label is None:
        raise ValueError(f"sample {sample['fight_id']} missing {target!r} label")
    probability = float(np.clip(model_probability, 0.001, 0.999))
    predicted_label = 1 if probability >= 0.5 else 0
    confidence = probability if predicted_label == 1 else 1 - probability
    market_probability = _prop_market_probability(prop_markets, str(sample["fight_id"]), target)
    market_predicted_label = None if market_probability is None else 1 if market_probability >= 0.5 else 0
    picked_market_probability = None
    picked_model_market_edge = None
    decimal_odds = None
    net_profit = None
    if market_probability is not None:
        picked_market_probability = market_probability if predicted_label == 1 else 1 - market_probability
        picked_model_market_edge = confidence - picked_market_probability
        decimal_odds = 1 / picked_market_probability
        net_profit = decimal_odds - 1 if predicted_label == actual_label else -1.0
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "target": target,
        "fighter_a_probability": probability,
        "model_probability": model_probability,
        "market_probability": market_probability,
        "actual_label": actual_label,
        "predicted_label": predicted_label,
        "market_predicted_label": market_predicted_label,
        "confidence": confidence,
        "picked_model_probability": confidence,
        "picked_market_probability": picked_market_probability,
        "picked_model_market_edge": picked_model_market_edge,
        "won": predicted_label == actual_label,
        "decimal_odds": decimal_odds,
        "net_profit": net_profit,
    }


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
    predicted_label = int(prediction["predicted_label"])
    market_predicted_label = 1 if market_probability >= 0.5 else 0
    picked_fighter_id = sample["fighter_a_id"] if predicted_label == 1 else sample["fighter_b_id"]
    picked_model_probability = probability if predicted_label == 1 else 1 - probability
    picked_market_probability = float(market[picked_fighter_id]["market_prob"])
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "target": "winner",
        "fighter_a_probability": prediction["fighter_a_probability"],
        "model_probability": model_probability,
        "market_probability": market_probability,
        "actual_label": sample["label"],
        "predicted_label": prediction["predicted_label"],
        "market_predicted_label": market_predicted_label,
        "confidence": prediction["confidence"],
        "picked_model_probability": picked_model_probability,
        "picked_market_probability": picked_market_probability,
        "picked_model_market_edge": picked_model_probability - picked_market_probability,
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
            "target": _target(variant),
            "features": variant["features"],
            "feature_names": _feature_names(variant),
            "market_blend_weight": variant.get("market_blend_weight"),
            "model_params": _model_params(variant),
            "calibration": _calibration(variant),
            "selection_policy": _selection_policy(variant),
            "feature_count": _feature_count(variant),
        },
        "events_scored": len({prediction["event_id"] for prediction in predictions}),
        "metrics": _safe_metrics(predictions),
        "simulated_research_roi": _target_roi(_target(variant), predictions),
    }


def _annotate_variant(report: dict[str, Any], market: dict[str, Any], gate: dict[str, Any]) -> None:
    if report["params"]["target"] != market["params"]["target"]:
        report["roi_delta_vs_market"] = None
        report["log_loss_delta_vs_market"] = None
        report["brier_delta_vs_market"] = None
        report["rejection_reasons"] = ["market_baseline_unavailable_for_target"]
        report["clears_market_gate"] = False
        return
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


def _target_roi(target: str, predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if target == "winner":
        return _roi(predictions)
    market_backed = [prediction for prediction in predictions if prediction.get("net_profit") is not None]
    if market_backed:
        roi = _roi(market_backed)
        return {
            **roi,
            "selected_entries": len(predictions),
            "market_backed_entries": len(market_backed),
        }
    return {
        "entries": 0,
        "wins": None,
        "units": None,
        "roi_pct": None,
        "stake_unit": "flat_1u",
        "status": f"{target}_market_odds_unavailable",
    }


def _recommendation(ranked: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = [row for row in ranked if row["name"] != "market_favorite"]
    clearing = [row for row in candidates if row["clears_market_gate"]]
    if clearing:
        best_clearing = clearing[0]
        return {
            "status": "candidate_for_locked_evaluation",
            "reason": f"{best_clearing['name']} clears the configured discovery gate; evaluate on a locked future slice before activation.",
        }
    best = candidates[0] if candidates else None
    if best is None:
        return {"status": "no_candidates", "reason": "No non-market variants were configured."}
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
        _target(variant),
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
        if variant["model"] in {"market_favorite", "prop_market_baseline"}:
            return {"base": "none"}
        raise ValueError("non-market variants cannot use features='none'")
    if features in {
        "production",
        "production_plus_availability",
        "production_plus_opponent_adjusted_recent_performance",
        "production_plus_style_matchup_pressure",
        "production_plus_market_context",
        "production_plus_all_research",
        "production_plus_all_research_market_context",
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
    if features == "production_plus_style_matchup_pressure":
        return [*FEATURE_NAMES, *STYLE_MATCHUP_PRESSURE_FEATURE_NAMES]
    if features == "production_plus_market_context":
        return [*FEATURE_NAMES, *MARKET_CONTEXT_FEATURE_NAMES]
    if features == "production_plus_all_research":
        return [
            *FEATURE_NAMES,
            *AVAILABILITY_FEATURE_NAMES,
            *OPPONENT_ADJUSTED_RECENT_PERFORMANCE_FEATURE_NAMES,
            *STYLE_MATCHUP_PRESSURE_FEATURE_NAMES,
        ]
    if features == "production_plus_all_research_market_context":
        return [
            *FEATURE_NAMES,
            *AVAILABILITY_FEATURE_NAMES,
            *OPPONENT_ADJUSTED_RECENT_PERFORMANCE_FEATURE_NAMES,
            *STYLE_MATCHUP_PRESSURE_FEATURE_NAMES,
            *MARKET_CONTEXT_FEATURE_NAMES,
        ]
    raise ValueError(f"unsupported feature set {features!r}")


def _base_feature_fn(features: str) -> FeatureFn:
    if features == "production":
        return _base_features
    if features == "production_plus_availability":
        return _availability_augmented_features
    if features == "production_plus_opponent_adjusted_recent_performance":
        return _opponent_adjusted_recent_performance_features
    if features == "production_plus_style_matchup_pressure":
        return _style_matchup_pressure_features
    if features == "production_plus_market_context":
        return _market_context_features
    if features == "production_plus_all_research":
        return _all_research_features
    if features == "production_plus_all_research_market_context":
        return _all_research_market_context_features
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


def _style_matchup_pressure_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate(
        [
            sample["features"],
            build_style_matchup_pressure_features(
                sample["fighter_a_id"],
                sample["fighter_b_id"],
                sample["event_date"],
            ),
        ]
    )


def _all_research_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate(
        [
            sample["features"],
            _availability_augmented_features(sample)[len(FEATURE_NAMES) :],
            build_opponent_adjusted_recent_performance_features(
                sample["fighter_a_id"],
                sample["fighter_b_id"],
                sample["event_date"],
            ),
            build_style_matchup_pressure_features(
                sample["fighter_a_id"],
                sample["fighter_b_id"],
                sample["event_date"],
            ),
        ]
    )


def _market_context_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate([sample["features"], np.array(sample["market_context_features"], dtype=float)])


def _all_research_market_context_features(sample: dict[str, Any]) -> np.ndarray:
    return np.concatenate(
        [
            _all_research_features(sample),
            np.array(sample["market_context_features"], dtype=float),
        ]
    )


def _attach_market_context(
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> list[dict[str, Any]]:
    enriched = []
    for sample in samples:
        market = markets[sample["fight_id"]]
        fighter_a_probability = float(market[sample["fighter_a_id"]]["market_prob"])
        fighter_b_probability = float(market[sample["fighter_b_id"]]["market_prob"])
        enriched.append(
            {
                **sample,
                "market_context_features": np.array(
                    [
                        fighter_a_probability,
                        fighter_b_probability,
                        fighter_a_probability - fighter_b_probability,
                        min(fighter_a_probability, fighter_b_probability),
                    ],
                    dtype=float,
                ),
            }
        )
    return enriched


def _attach_target_labels(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not samples:
        return []
    labels = _load_target_labels([sample["fight_id"] for sample in samples])
    return [
        {**sample, "target_labels": labels[sample["fight_id"]]}
        for sample in samples
        if sample["fight_id"] in labels
    ]


def _load_target_labels(fight_ids: list[str]) -> dict[str, dict[str, int]]:
    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    fr.fight_id,
                    fr.method
                FROM fight_results fr
                WHERE fr.fight_id = ANY(%s)
                    AND fr.outcome IN ('win', 'loss')
                """,
                (fight_ids,),
            )
            rows = cur.fetchall()
    by_fight: dict[str, list[str]] = {}
    for row in rows:
        method = str(row["method"] or "").strip().lower()
        if method:
            by_fight.setdefault(str(row["fight_id"]), []).append(method)
    labels = {}
    for fight_id, methods in by_fight.items():
        decision = any("decision" in method for method in methods)
        labels[fight_id] = {
            "decision": 1 if decision else 0,
            "finish": 0 if decision else 1,
        }
    return labels


def _target_label(sample: dict[str, Any], target: str) -> int | None:
    if target == "winner":
        return int(sample["label"])
    labels = sample.get("target_labels") or {}
    value = labels.get(target)
    return None if value is None else int(value)


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


def _target(variant: dict[str, Any]) -> str:
    target = str(variant.get("target") or "winner")
    if target not in SUPPORTED_TARGETS:
        raise ValueError(f"unsupported target {target!r}")
    if variant["model"] == "market_favorite" and target != "winner":
        raise ValueError("market_favorite baseline only supports target='winner'")
    return target


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
