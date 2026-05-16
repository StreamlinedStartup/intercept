"""Generate a report-only fresh-corpus selected-fight winner search."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ml.generate_additional_winner_search import build_config as build_additional_winner_config
from ml.train import REPO_ROOT

DEFAULT_OUTPUT = REPO_ROOT / "configs" / "experiments" / "fresh-winner-search-v1.json"


def build_config() -> dict[str, Any]:
    config = build_additional_winner_config()
    config["name"] = "fresh-winner-search-v1"
    config["description"] = (
        "Expanded report-only selected-fight search over imported post-holdout "
        "FightOdds UFC events."
    )
    config["corpus"]["holdout"] = {
        "type": "after_date",
        "after_date": "2024-03-09",
    }
    config["split"] = {
        "policy": "chronological_walk_forward",
        "candidate_selection": "fresh_post_holdout_corpus",
        "locked_evaluation": "future_required",
    }
    config["outputs"] = {
        "json": "data/experiments/harness/fresh-winner-search-v1.json",
        "markdown": "data/experiments/harness/fresh-winner-search-v1.md",
    }
    for variant in config["variants"]:
        if variant["name"] != "market_favorite":
            variant["description"] = (
                "Fresh-corpus selected-fight logistic search candidate; report-only."
            )
    return config


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate fresh selected-fight winner search config")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config = build_config()
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(REPO_ROOT)), "variants": len(config["variants"])}, indent=2))


if __name__ == "__main__":
    main()
