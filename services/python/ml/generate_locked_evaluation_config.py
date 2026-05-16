"""Generate the locked-style holdout evaluation config from frozen candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ml.train import REPO_ROOT

DEFAULT_CANDIDATES = REPO_ROOT / "configs" / "experiments" / "locked-evaluation-candidates-v1.json"
DEFAULT_OUTPUT = REPO_ROOT / "configs" / "experiments" / "locked-evaluation-v1.json"


def build_config(candidates_path: Path = DEFAULT_CANDIDATES) -> dict[str, Any]:
    candidates = json.loads(candidates_path.read_text())
    holdout = candidates["holdout_policy"]
    variants = [
        {
            "name": "market_favorite",
            "model": "market_favorite",
            "features": "none",
            "market_blend_weight": None,
            "description": "No-vig market favorite baseline.",
        }
    ]
    for candidate in candidates["candidates"]:
        variants.append(
            {
                "name": candidate["name"],
                "model": candidate["model"],
                "features": candidate["features"],
                "market_blend_weight": candidate["market_blend_weight"],
                "model_params": candidate["model_params"],
                "calibration": candidate["calibration"],
                "selection_policy": candidate["selection_policy"],
                "description": candidate["description"],
            }
        )
    return {
        "name": "locked-evaluation-v1",
        "description": "Frozen selected-fight candidates evaluated on a last-10-event historical locked-style holdout.",
        "value_status": "research_only",
        "report_only": True,
        "writes_model_versions": False,
        "corpus": {
            "source": "matched_market_fights",
            "market_source": "fightodds_no_vig_consensus",
            "min_train_samples": 20,
            "max_events": None,
            "holdout": {
                "type": holdout["type"],
                "event_count": holdout["event_count"],
            },
        },
        "split": {
            "policy": "chronological_walk_forward",
            "candidate_selection": "full_current_corpus",
            "locked_evaluation": "none_current_corpus",
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
            "json": "data/experiments/harness/locked-evaluation-v1.json",
            "markdown": "data/experiments/harness/locked-evaluation-v1.md",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate locked-style evaluation config")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    candidates_path = args.candidates if args.candidates.is_absolute() else REPO_ROOT / args.candidates
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    config = build_config(candidates_path)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(REPO_ROOT)), "variants": len(config["variants"])}, indent=2))


if __name__ == "__main__":
    main()
