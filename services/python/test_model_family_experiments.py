"""Tests for report-only model-family experiment helpers."""
from __future__ import annotations

import pytest

from ml.model_family_experiments import _annotate_candidate, _rejection_reasons, _without


def test_without_removes_selected_features_only() -> None:
    assert _without(["a", "b", "c"], {"b", "d"}) == ["a", "c"]


def test_rejection_reasons_block_roi_and_calibration_regression() -> None:
    report = {
        "name": "candidate",
        "events_scored": 37,
        "metrics": {
            "count": 345,
            "log_loss": 0.7,
            "brier_score": 0.2,
            "abs_calibration_error": 0.1,
        },
        "roi_delta_vs_market_favorite": 0.01,
    }
    market = {"log_loss": 0.6, "brier_score": 0.19, "abs_calibration_error": 0.08}

    assert _rejection_reasons(report, market) == [
        "roi_delta_below_plus_2pp_market_gate",
        "log_loss_worse_than_market",
        "brier_worse_than_market",
        "calibration_worse_than_market",
    ]


def test_annotate_candidate_marks_clean_candidate_as_gate_clear() -> None:
    report = {
        "name": "candidate",
        "events_scored": 37,
        "metrics": {
            "count": 345,
            "log_loss": 0.5,
            "brier_score": 0.18,
            "abs_calibration_error": 0.02,
        },
        "simulated_research_roi": {"roi_pct": 0.19},
    }
    market = {"log_loss": 0.6, "brier_score": 0.19, "abs_calibration_error": 0.08}

    _annotate_candidate(report, 0.16, market)

    assert report["roi_delta_vs_market_favorite"] == pytest.approx(0.03)
    assert report["rejection_reasons"] == []
    assert report["clears_market_roi_gate"] is True
