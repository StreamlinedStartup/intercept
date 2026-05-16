import numpy as np

from ml import prop_indicators


def setup_function():
    prop_indicators._load_over_2_5_artifact.cache_clear()


def _artifact(training_sample_count: int = 4) -> dict:
    return {
        "model_version": "locked_over_2_5_positive_log_c1_conf58",
        "target": "over_2_5",
        "label": "Over 2.5 rounds",
        "generated_at": "2026-05-16T00:00:00+00:00",
        "training_sample_count": training_sample_count,
        "threshold": 0.58,
        "calibration": {"method": "temperature", "temperature": 1.6},
        "imputer_statistics": [0.0],
        "scaler_mean": [0.0],
        "scaler_scale": [1.0],
        "coef": [2.0],
        "intercept": 0.0,
    }


def _patch_live_features(monkeypatch):
    monkeypatch.setattr(
        prop_indicators,
        "_live_sample",
        lambda fighter_a_id, fighter_b_id, fight_date, target_weight_class: {
            "fight_id": "live",
            "event_id": "live",
            "event_date": fight_date,
            "fighter_a_id": fighter_a_id,
            "fighter_b_id": fighter_b_id,
            "features": np.array([5.0], dtype=float),
        },
    )
    monkeypatch.setattr(
        prop_indicators,
        "_feature_fn",
        lambda _variant: lambda sample: np.array(sample["features"], dtype=float),
    )


def test_over_2_5_indicator_uses_frozen_artifact_threshold(monkeypatch):
    monkeypatch.setattr(prop_indicators, "_load_over_2_5_artifact", lambda: _artifact())
    _patch_live_features(monkeypatch)

    result = prop_indicators.over_2_5_indicator(
        "fighter-a",
        "fighter-b",
        "2026-06-01",
        "Welterweight",
        min_train_samples=4,
    )

    assert result["target"] == "over_2_5"
    assert result["model_version"] == "locked_over_2_5_positive_log_c1_conf58"
    assert result["threshold"] == 0.58
    assert result["candidate"] is True
    assert result["value_status"] == "report_only"
    assert result["training_sample_count"] == 4
    assert result["artifact_generated_at"] == "2026-05-16T00:00:00+00:00"


def test_over_2_5_indicator_reports_insufficient_training(monkeypatch):
    monkeypatch.setattr(prop_indicators, "_load_over_2_5_artifact", lambda: _artifact(0))

    result = prop_indicators.over_2_5_indicator(
        "fighter-a",
        "fighter-b",
        "2026-06-01",
        min_train_samples=4,
    )

    assert result["candidate"] is False
    assert result["model_probability"] is None
    assert result["value_status"] == "insufficient_training"
    assert result["training_sample_count"] == 0


def test_over_2_5_artifact_probability_matches_pipeline_math():
    probability = prop_indicators._artifact_probability(
        np.array([float("nan")], dtype=float),
        {
            "imputer_statistics": [2.0],
            "scaler_mean": [1.0],
            "scaler_scale": [2.0],
            "coef": [4.0],
            "intercept": -1.0,
        },
    )

    assert round(probability, 6) == round(1 / (1 + np.exp(-1)), 6)
