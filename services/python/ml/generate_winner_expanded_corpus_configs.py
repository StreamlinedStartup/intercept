"""Generate frozen-winner configs for expanded corpus retests."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ml.train import REPO_ROOT

MIN_TRAIN_SAMPLES = [20, 40, 60, 80, 100]
WINNER_VARIANT = {
    "name": "log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63",
    "model": "logistic_regression",
    "features": "production_plus_all_research_market_context",
    "market_blend_weight": 0.45,
    "model_params": {"C": 2.5},
    "calibration": {"method": "temperature", "temperature": 2.2},
    "selection_policy": {"type": "min_confidence", "threshold": 0.63},
    "description": "Frozen gate-clearing candidate retested across expanded eligible corpus windows.",
}


def build_config(min_train_samples: int) -> dict[str, Any]:
    return {
        "name": f"winner-expanded-corpus-mintrain-{min_train_samples}",
        "description": f"Frozen winner retest with min_train_samples={min_train_samples}.",
        "value_status": "research_only",
        "report_only": True,
        "writes_model_versions": False,
        "corpus": {
            "source": "matched_market_fights",
            "market_source": "fightodds_no_vig_consensus",
            "min_train_samples": min_train_samples,
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
        "variants": [
            {
                "name": "market_favorite",
                "model": "market_favorite",
                "features": "none",
                "market_blend_weight": None,
                "description": "No-vig market favorite baseline.",
            },
            WINNER_VARIANT,
        ],
        "outputs": {
            "json": f"data/experiments/harness/winner-expanded-corpus-mintrain-{min_train_samples}.json",
            "markdown": f"data/experiments/harness/winner-expanded-corpus-mintrain-{min_train_samples}.md",
        },
    }


def write_configs(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for min_train_samples in MIN_TRAIN_SAMPLES:
        path = output_dir / f"winner-expanded-corpus-mintrain-{min_train_samples}.json"
        path.write_text(json.dumps(build_config(min_train_samples), indent=2) + "\n")
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate frozen winner expanded-corpus configs")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "configs" / "experiments")
    args = parser.parse_args()

    output_dir = args.output_dir if args.output_dir.is_absolute() else REPO_ROOT / args.output_dir
    paths = write_configs(output_dir)
    print(
        json.dumps(
            {
                "configs": [str(path.relative_to(REPO_ROOT)) for path in paths],
                "min_train_samples": MIN_TRAIN_SAMPLES,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
