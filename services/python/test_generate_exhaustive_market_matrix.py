"""Tests for exhaustive market matrix generation."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml.experiment_harness import _validate_config
from ml.generate_exhaustive_market_matrix import build_config


def test_exhaustive_market_matrix_is_research_only_and_unique() -> None:
    config = build_config()
    names = [variant["name"] for variant in config["variants"]]

    _validate_config(config)

    assert config["report_only"] is True
    assert config["writes_model_versions"] is False
    assert config["value_status"] == "research_only"
    assert len(names) == len(set(names))
    assert len(names) == 42281
    assert "production_plus_market_context" in {variant["features"] for variant in config["variants"]}
    assert "production_plus_all_research_market_context" in {variant["features"] for variant in config["variants"]}
