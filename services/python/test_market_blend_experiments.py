"""Tests for report-only market-aware blend experiments."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from ml.market_blend_experiments import blend_probability, roi_delta, shrink_to_even


def test_blend_probability_weights_model_and_market() -> None:
    assert blend_probability(0.8, 0.6, 0.25) == pytest.approx(0.65)
    assert blend_probability(0.8, 0.6, 0.0) == 0.6
    assert blend_probability(0.8, 0.6, 1.0) == 0.8


def test_shrink_to_even_moves_probability_toward_half() -> None:
    assert shrink_to_even(0.9, 0.25) == 0.8
    assert shrink_to_even(0.9, 0.5) == 0.7
    assert shrink_to_even(0.1, 0.5) == 0.3


def test_roi_delta_handles_missing_values() -> None:
    assert roi_delta(0.18, 0.16) == 0.01999999999999999
    assert roi_delta(None, 0.16) is None
    assert roi_delta(0.18, None) is None
