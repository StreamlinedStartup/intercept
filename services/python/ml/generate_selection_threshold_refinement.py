"""Generate a focused confidence-threshold refinement matrix."""
from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any

from ml.generate_exhaustive_market_matrix import _blend_name, _calibration_name, _feature_name, _model_name, _number
from ml.generate_selection_gate_matrix import _selection_name
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "configs" / "experiments" / "market-grid-selection-threshold-v1.json"


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
    for c, temperature, blend_weight, threshold in product(
        [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
        [1.6, 1.8, 2.0, 2.2, 2.5],
        [0.4, 0.45, 0.5, 0.55, 0.6],
        [0.61, 0.62, 0.63, 0.64, 0.65],
    ):
        calibration = {"method": "temperature", "temperature": temperature}
        selection_policy = {"type": "min_confidence", "threshold": threshold}
        params = {"C": c}
        variants.append(
            {
                "name": "_".join(
                    [
                        _model_name("logistic_regression"),
                        _feature_name("production_plus_all_research_market_context"),
                        f"c{_number(c)}",
                        _calibration_name(calibration),
                        _blend_name(blend_weight),
                        _selection_name(selection_policy),
                    ]
                ),
                "model": "logistic_regression",
                "features": "production_plus_all_research_market_context",
                "market_blend_weight": blend_weight,
                "model_params": params,
                "calibration": calibration,
                "selection_policy": selection_policy,
                "description": "Focused all-research market-context logistic confidence threshold refinement.",
            }
        )
    names = [variant["name"] for variant in variants]
    if len(names) != len(set(names)):
        raise ValueError("generated variant names are not unique")
    return {
        "name": "market-grid-selection-threshold-v1",
        "description": "Focused report-only threshold refinement around the best v1 selected-fight near miss.",
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
            "json": "data/experiments/harness/market-grid-selection-threshold-v1.json",
            "markdown": "data/experiments/harness/market-grid-selection-threshold-v1.md",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate selection threshold refinement config")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config = build_config()
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(REPO_ROOT)), "variants": len(config["variants"])}, indent=2))


if __name__ == "__main__":
    main()
