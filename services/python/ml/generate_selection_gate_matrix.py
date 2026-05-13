"""Generate a targeted report-only selection-policy gate search matrix."""
from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any

from ml.generate_exhaustive_market_matrix import _blend_name, _calibration_name, _feature_name, _model_name, _number
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "configs" / "experiments" / "market-grid-selection-v1.json"

FEATURE_SETS = [
    "production_plus_market_context",
    "production_plus_all_research_market_context",
]
XGBOOST_PARAM_GRID = [
    {"n_estimators": n, "max_depth": depth, "learning_rate": lr, "subsample": subsample, "colsample_bytree": colsample}
    for n, depth, lr, subsample, colsample in product(
        [20, 40, 80],
        [1, 2, 3, 4],
        [0.05, 0.1],
        [0.8, 1.0],
        [0.8, 1.0],
    )
]
LOGISTIC_PARAM_GRID = [{"C": value} for value in [0.1, 0.25, 0.5, 1.0, 2.0, 5.0]]
CALIBRATIONS = [
    {"method": "none"},
    {"method": "temperature", "temperature": 1.1},
    {"method": "temperature", "temperature": 1.25},
    {"method": "temperature", "temperature": 1.5},
    {"method": "temperature", "temperature": 2.0},
]
MARKET_BLEND_WEIGHTS = [None, 0.01, 0.05, 0.1, 0.25, 0.5]
SELECTION_POLICIES = [
    {"type": "all"},
    {"type": "market_favorite_only"},
    {"type": "market_underdog_only"},
    {"type": "model_market_agree"},
    {"type": "model_market_disagree"},
    {"type": "min_confidence", "threshold": 0.55},
    {"type": "min_confidence", "threshold": 0.6},
    {"type": "min_confidence", "threshold": 0.65},
    {"type": "min_model_market_edge", "threshold": 0.01},
    {"type": "min_model_market_edge", "threshold": 0.03},
    {"type": "min_absolute_model_market_edge", "threshold": 0.03},
    {"type": "min_absolute_model_market_edge", "threshold": 0.05},
]


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
        for params in XGBOOST_PARAM_GRID:
            for calibration in CALIBRATIONS:
                for blend_weight in MARKET_BLEND_WEIGHTS:
                    for selection_policy in SELECTION_POLICIES:
                        variants.append(
                            _variant(
                                model="xgboost",
                                features=features,
                                params=params,
                                calibration=calibration,
                                blend_weight=blend_weight,
                                selection_policy=selection_policy,
                            )
                        )
        for params in LOGISTIC_PARAM_GRID:
            for calibration in CALIBRATIONS:
                for blend_weight in MARKET_BLEND_WEIGHTS:
                    for selection_policy in SELECTION_POLICIES:
                        variants.append(
                            _variant(
                                model="logistic_regression",
                                features=features,
                                params=params,
                                calibration=calibration,
                                blend_weight=blend_weight,
                                selection_policy=selection_policy,
                            )
                        )
    names = [variant["name"] for variant in variants]
    if len(names) != len(set(names)):
        raise ValueError("generated variant names are not unique")
    return {
        "name": "market-grid-selection-v1",
        "description": "Report-only selection-policy search over market-context model variants, with selected-fight market baselines.",
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
            "json": "data/experiments/harness/market-grid-selection-v1.json",
            "markdown": "data/experiments/harness/market-grid-selection-v1.md",
        },
    }


def _variant(
    *,
    model: str,
    features: str,
    params: dict[str, Any],
    calibration: dict[str, Any],
    blend_weight: float | None,
    selection_policy: dict[str, Any],
) -> dict[str, Any]:
    variant: dict[str, Any] = {
        "name": "_".join(
            [
                _model_name(model),
                _feature_name(features),
                _params_name(params),
                _calibration_name(calibration),
                _blend_name(blend_weight),
                _selection_name(selection_policy),
            ]
        ),
        "model": model,
        "features": features,
        "market_blend_weight": blend_weight,
        "model_params": params,
        "selection_policy": selection_policy,
        "description": f"{model} using {features} with {selection_policy['type']} selection.",
    }
    if calibration["method"] != "none":
        variant["calibration"] = calibration
    return variant


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


def _selection_name(policy: dict[str, Any]) -> str:
    if "threshold" not in policy:
        return policy["type"]
    return f"{policy['type']}{_number(policy['threshold'])}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate selection-policy market experiment config")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config = build_config()
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(REPO_ROOT)), "variants": len(config["variants"])}, indent=2))


if __name__ == "__main__":
    main()
