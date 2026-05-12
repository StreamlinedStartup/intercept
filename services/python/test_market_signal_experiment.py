"""Tests for feature availability signal experiment helpers."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from ml.features import FEATURE_NAMES
from ml.market_signal_experiment import (
    AVAILABILITY_FEATURE_NAMES,
    _availability_augmented_features,
    _availability_features,
    _recommendation,
    render_markdown,
)


def _sample(features: np.ndarray) -> dict:
    return {"features": features}


def test_availability_features_are_prefight_missingness_indicators() -> None:
    features = np.zeros(len(FEATURE_NAMES), dtype=float)
    features[FEATURE_NAMES.index("wins_last_3_diff")] = np.nan
    features[FEATURE_NAMES.index("wins_last_5_diff")] = np.nan

    values = _availability_features(_sample(features))

    assert values.tolist() == [2.0, 2.0 / len(FEATURE_NAMES), 0.0, 1.0]


def test_augmented_feature_vector_appends_in_stable_order() -> None:
    features = np.arange(len(FEATURE_NAMES), dtype=float)

    augmented = _availability_augmented_features(_sample(features))

    assert len(augmented) == len(FEATURE_NAMES) + len(AVAILABILITY_FEATURE_NAMES)
    assert np.array_equal(augmented[: len(FEATURE_NAMES)], features)
    assert augmented[-4:].tolist() == [0.0, 0.0, 1.0, 1.0]


def test_recommendation_does_not_promote_when_probability_metrics_degrade() -> None:
    candidate = {
        "metrics": {"accuracy": 0.45, "log_loss": 0.8, "brier_score": 0.3},
        "simulated_research_roi": {"roi_pct": -0.1},
    }
    baseline = {
        "metrics": {"accuracy": 0.5, "log_loss": 0.7, "brier_score": 0.25},
        "simulated_research_roi": {"roi_pct": -0.08},
    }
    market = {
        "metrics": {"accuracy": 0.7, "log_loss": 0.55, "brier_score": 0.18},
        "simulated_research_roi": {"roi_pct": 0.2},
    }

    recommendation = _recommendation(candidate, baseline, market)

    assert recommendation["status"] == "do_not_promote"


def test_markdown_includes_report_only_contract() -> None:
    report = {
        "generated_at": "2026-05-12T00:00:00+00:00",
        "value_status": "research_only",
        "writes_model_versions": False,
        "signal": {"name": "pre_fight_feature_availability_flags"},
        "coverage": {"model_eligible_events": 1, "model_eligible_fights": 1},
        "strategies": [
            {
                "name": "market_favorite",
                "metrics": {"count": 1, "accuracy": 1.0, "log_loss": 0.1, "brier_score": 0.1},
                "simulated_research_roi": {"roi_pct": 0.1},
            }
        ],
        "deltas": {
            "candidate_vs_market": {"roi_delta": -0.1, "log_loss_delta": 0.1, "brier_delta": 0.1},
            "candidate_vs_current_model": {"roi_delta": 0.0, "log_loss_delta": 0.0, "brier_delta": 0.0},
        },
        "target_cluster_checks": [],
        "recommendation": {"status": "do_not_promote", "reason": "test"},
        "policy": "No model_versions writes.",
    }

    markdown = render_markdown(report)

    assert "Writes `model_versions`: `false`" in markdown
    assert "pre_fight_feature_availability_flags" in markdown
