from datetime import date

import numpy as np

from ml import prop_indicators


def _sample(fight_id: str, event_date: str, feature: float, label: int) -> dict:
    return {
        "fight_id": fight_id,
        "event_id": f"event-{fight_id}",
        "event_date": date.fromisoformat(event_date),
        "fighter_a_id": f"a-{fight_id}",
        "fighter_b_id": f"b-{fight_id}",
        "features": np.array([feature], dtype=float),
        "target_labels": {"over_2_5": label},
    }


def test_over_2_5_indicator_uses_frozen_threshold(monkeypatch):
    monkeypatch.setattr(
        prop_indicators,
        "_training_samples",
        lambda: [
            _sample("1", "2025-01-01", 0.0, 0),
            _sample("2", "2025-02-01", 1.0, 0),
            _sample("3", "2025-03-01", 3.0, 1),
            _sample("4", "2025-04-01", 4.0, 1),
        ],
    )
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


def test_over_2_5_indicator_reports_insufficient_training(monkeypatch):
    monkeypatch.setattr(prop_indicators, "_training_samples", lambda: [])

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
