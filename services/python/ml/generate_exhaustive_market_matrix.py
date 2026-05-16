"""Generate the report-only exhaustive market gate search matrix."""
from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any

from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "configs" / "experiments" / "market-grid-exhaustive-v2.json"

FEATURE_SETS = [
    "production",
    "production_plus_availability",
    "production_plus_opponent_adjusted_recent_performance",
    "production_plus_style_matchup_pressure",
    "production_plus_market_context",
    "production_plus_all_research",
    "production_plus_all_research_market_context",
]
FEATURE_SUBSETS = [
    None,
]
XGBOOST_PARAM_GRID = [
    {"n_estimators": n, "max_depth": depth, "learning_rate": lr, "subsample": subsample, "colsample_bytree": colsample}
    for n, depth, lr, subsample, colsample in product(
        [20, 40, 80],
        [1, 2, 3, 4],
        [0.03, 0.05, 0.1],
        [0.8, 1.0],
        [0.8, 1.0],
    )
]
LOGISTIC_PARAM_GRID = [{"C": value} for value in [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]]
CALIBRATIONS = [
    {"method": "none"},
    {"method": "temperature", "temperature": 1.1},
    {"method": "temperature", "temperature": 1.25},
    {"method": "temperature", "temperature": 1.5},
    {"method": "temperature", "temperature": 2.0},
]
MARKET_BLEND_WEIGHTS = [None, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75]


def build_config() -> dict[str, Any]:
    variants: list[dict[str, Any]] = [
        {
            "name": "market_favorite",
            "model": "market_favorite",
            "features": "none",
            "market_blend_weight": None,
            "description": "No-vig market favorite baseline.",
        }
    ]
    for features in FEATURE_SETS:
        for feature_subset in FEATURE_SUBSETS:
            for params in XGBOOST_PARAM_GRID:
                for calibration in CALIBRATIONS:
                    for blend_weight in MARKET_BLEND_WEIGHTS:
                        variants.append(
                            _variant(
                                model="xgboost",
                                features=features,
                                params=params,
                                calibration=calibration,
                                feature_subset=feature_subset,
                                blend_weight=blend_weight,
                            )
                        )
            for params in LOGISTIC_PARAM_GRID:
                for calibration in CALIBRATIONS:
                    for blend_weight in MARKET_BLEND_WEIGHTS:
                        variants.append(
                            _variant(
                                model="logistic_regression",
                                features=features,
                                params=params,
                                calibration=calibration,
                                feature_subset=feature_subset,
                                blend_weight=blend_weight,
                            )
                        )
    names = [variant["name"] for variant in variants]
    if len(names) != len(set(names)):
        raise ValueError("generated variant names are not unique")
    return {
        "name": "market-grid-exhaustive-v2",
        "description": "Exhaustive report-only sweep across supported model families, market-context features, feature subsets, calibration settings, and market blend weights.",
        "value_status": "research_only",
        "report_only": True,
        "writes_model_versions": False,
        "corpus": {
            "source": "matched_market_fights",
            "market_source": "fightodds_no_vig_consensus",
            "min_train_samples": 100,
            "max_events": None,
        },
        "split": {
            "policy": "chronological_walk_forward",
            "candidate_selection": "full_current_corpus",
            "locked_evaluation": "future_required",
        },
        "gate": {
            "baseline": "market_favorite",
            "min_roi_delta_vs_market": 0.02,
            "probability_quality": {
                "require_log_loss_not_worse": True,
                "require_brier_not_worse": True,
            },
        },
        "variants": variants,
        "outputs": {
            "json": "data/experiments/harness/market-grid-exhaustive-v2.json",
            "markdown": "data/experiments/harness/market-grid-exhaustive-v2.md",
        },
    }


def _variant(
    *,
    model: str,
    features: str,
    params: dict[str, Any],
    calibration: dict[str, Any],
    feature_subset: dict[str, Any] | None,
    blend_weight: float | None,
) -> dict[str, Any]:
    parts = [
        _model_name(model),
        _feature_name(features),
        _params_name(params),
        _subset_name(feature_subset),
        _calibration_name(calibration),
        _blend_name(blend_weight),
    ]
    variant: dict[str, Any] = {
        "name": "_".join(part for part in parts if part),
        "model": model,
        "features": features,
        "market_blend_weight": blend_weight,
        "model_params": params,
        "description": f"{model} using {features}.",
    }
    if calibration["method"] != "none":
        variant["calibration"] = calibration
    if feature_subset is not None:
        variant["feature_subset"] = feature_subset
    return variant


def _model_name(model: str) -> str:
    return {"xgboost": "xgb", "logistic_regression": "log"}[model]


def _feature_name(features: str) -> str:
    return {
        "production": "prod",
        "production_plus_availability": "avail",
        "production_plus_opponent_adjusted_recent_performance": "oarp",
        "production_plus_style_matchup_pressure": "smp",
        "production_plus_market_context": "marketctx",
        "production_plus_all_research": "allresearch",
        "production_plus_all_research_market_context": "allmarketctx",
    }[features]


def _params_name(params: dict[str, Any]) -> str:
    if "C" in params:
        return f"c{_number(params['C'])}"
    return "n{n}_d{d}_lr{lr}_ss{ss}_cs{cs}".format(
        n=params["n_estimators"],
        d=params["max_depth"],
        lr=_number(params["learning_rate"]),
        ss=_number(params["subsample"]),
        cs=_number(params["colsample_bytree"]),
    )


def _subset_name(feature_subset: dict[str, Any] | None) -> str:
    if feature_subset is None:
        return "all"
    prefix = "only" if feature_subset["mode"] == "only" else "no"
    return f"{prefix}{'-'.join(feature_subset['names'])}"


def _calibration_name(calibration: dict[str, Any]) -> str:
    if calibration["method"] == "none":
        return "raw"
    return f"temp{_number(calibration['temperature'])}"


def _blend_name(blend_weight: float | None) -> str:
    if blend_weight is None:
        return "modelonly"
    return f"blend{int(round(blend_weight * 100)):02d}"


def _number(value: float | int) -> str:
    return str(value).replace(".", "p")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate exhaustive market experiment config")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config = build_config()
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(REPO_ROOT)), "variants": len(config["variants"])}, indent=2))


if __name__ == "__main__":
    main()
