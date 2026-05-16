"""Report-only prop indicator helpers."""
from __future__ import annotations

from datetime import date
from typing import Any

import numpy as np

from ml.features import build_feature_row
from ml.market_gate_report import _load_matched_market_samples
from ml.odds_aware_report import _load_source_coverage
from ml.experiment_harness import (
    _attach_target_labels,
    _calibrate_probability,
    _feature_fn,
    _model,
    _target_label,
)

OVER_2_5_TARGET = "over_2_5"
OVER_2_5_THRESHOLD = 0.58
OVER_2_5_MODEL_VERSION = "locked_over_2_5_positive_log_c1_conf58"

_OVER_2_5_VARIANT = {
    "name": OVER_2_5_MODEL_VERSION,
    "model": "logistic_regression",
    "target": OVER_2_5_TARGET,
    "features": "production_plus_all_research",
    "model_params": {"C": 1.0},
    "calibration": {"method": "temperature", "temperature": 1.6},
    "selection_policy": {"type": "positive_target_edge", "threshold": OVER_2_5_THRESHOLD},
}


def over_2_5_indicator(
    fighter_a_id: str,
    fighter_b_id: str,
    fight_date: str,
    target_weight_class: str | None = None,
    *,
    min_train_samples: int = 100,
) -> dict[str, Any]:
    """Return the frozen Over 2.5 report-only indicator for a future fight."""
    parsed_date = date.fromisoformat(fight_date)
    training_samples = [
        sample
        for sample in _training_samples()
        if sample["event_date"] < parsed_date
        and _target_label(sample, OVER_2_5_TARGET) is not None
    ]
    if len(training_samples) < min_train_samples:
        return _insufficient_training(len(training_samples), min_train_samples)

    train_y = np.array([_target_label(sample, OVER_2_5_TARGET) for sample in training_samples], dtype=int)
    if len(set(train_y.tolist())) < 2:
        return _insufficient_training(len(training_samples), min_train_samples)

    feature_fn = _feature_fn(_OVER_2_5_VARIANT)
    model = _model("logistic_regression", {"C": 1.0})
    train_x = np.vstack([feature_fn(sample) for sample in training_samples])
    model.fit(train_x, train_y)

    live_sample = _live_sample(fighter_a_id, fighter_b_id, parsed_date, target_weight_class)
    raw_probability = float(model.predict_proba(feature_fn(live_sample).reshape(1, -1))[0][1])
    probability = _calibrate_probability(raw_probability, _OVER_2_5_VARIANT["calibration"])

    return {
        "target": OVER_2_5_TARGET,
        "label": "Over 2.5 rounds",
        "model_version": OVER_2_5_MODEL_VERSION,
        "model_probability": probability,
        "threshold": OVER_2_5_THRESHOLD,
        "candidate": probability >= OVER_2_5_THRESHOLD,
        "value_status": "report_only",
        "value_status_reason": (
            "Locked validation passed; live forward tracking required before production betting activation."
        ),
        "training_sample_count": len(training_samples),
    }


def _training_samples() -> list[dict[str, Any]]:
    coverage = _load_source_coverage()
    return _attach_target_labels(_load_matched_market_samples(coverage))


def _live_sample(
    fighter_a_id: str,
    fighter_b_id: str,
    fight_date: date,
    target_weight_class: str | None,
) -> dict[str, Any]:
    return {
        "fight_id": "live",
        "event_id": "live",
        "event_date": fight_date,
        "fighter_a_id": fighter_a_id,
        "fighter_b_id": fighter_b_id,
        "features": build_feature_row(
            fighter_a_id,
            fighter_b_id,
            fight_date,
            target_weight_class,
        ),
    }


def _insufficient_training(found: int, required: int) -> dict[str, Any]:
    return {
        "target": OVER_2_5_TARGET,
        "label": "Over 2.5 rounds",
        "model_version": OVER_2_5_MODEL_VERSION,
        "model_probability": None,
        "threshold": OVER_2_5_THRESHOLD,
        "candidate": False,
        "value_status": "insufficient_training",
        "value_status_reason": f"Need at least {required} labeled Over 2.5 training fights; found {found}.",
        "training_sample_count": found,
    }
