"""Report-only prop indicator helpers."""
from __future__ import annotations

import json
import math
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from ml.features import build_feature_row
from ml.experiment_harness import (
    _calibrate_probability,
    _feature_fn,
)

OVER_2_5_TARGET = "over_2_5"
OVER_2_5_THRESHOLD = 0.58
OVER_2_5_MODEL_VERSION = "locked_over_2_5_positive_log_c1_conf58"
REPO_ROOT = Path(__file__).resolve().parents[3]
OVER_2_5_ARTIFACT_PATH = REPO_ROOT / "data" / "models" / f"{OVER_2_5_MODEL_VERSION}.json"

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
    artifact = _load_over_2_5_artifact()
    training_sample_count = int(artifact["training_sample_count"])
    if training_sample_count < min_train_samples:
        return _insufficient_training(training_sample_count, min_train_samples)

    live_sample = _live_sample(fighter_a_id, fighter_b_id, parsed_date, target_weight_class)
    features = _feature_fn(_OVER_2_5_VARIANT)(live_sample)
    raw_probability = _artifact_probability(features, artifact)
    probability = _calibrate_probability(raw_probability, artifact["calibration"])

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
        "training_sample_count": training_sample_count,
        "artifact_generated_at": artifact["generated_at"],
    }


@lru_cache(maxsize=16)
def _load_over_2_5_artifact() -> dict[str, Any]:
    if not OVER_2_5_ARTIFACT_PATH.exists():
        raise FileNotFoundError(f"Over 2.5 model artifact is missing: {OVER_2_5_ARTIFACT_PATH}")
    artifact = json.loads(OVER_2_5_ARTIFACT_PATH.read_text())
    if artifact.get("model_version") != OVER_2_5_MODEL_VERSION:
        raise ValueError(
            f"Over 2.5 artifact version mismatch: expected {OVER_2_5_MODEL_VERSION}, "
            f"got {artifact.get('model_version')}"
        )
    if artifact.get("target") != OVER_2_5_TARGET:
        raise ValueError(f"Over 2.5 artifact target mismatch: {artifact.get('target')}")
    return artifact


def _artifact_probability(features: np.ndarray, artifact: dict[str, Any]) -> float:
    values = np.asarray(features, dtype=float)
    imputed = _apply_imputer(values, artifact["imputer_statistics"])
    scaled = _apply_scaler(imputed, artifact["scaler_mean"], artifact["scaler_scale"])
    coef = np.asarray(artifact["coef"], dtype=float)
    if scaled.shape[0] != coef.shape[0]:
        raise ValueError(
            f"Over 2.5 artifact feature mismatch: expected {coef.shape[0]}, got {scaled.shape[0]}"
        )
    logit = float(np.dot(scaled, coef) + float(artifact["intercept"]))
    return 1 / (1 + math.exp(-logit))


def _apply_imputer(values: np.ndarray, medians: list[float]) -> np.ndarray:
    medians_array = np.asarray(medians, dtype=float)
    if values.shape[0] != medians_array.shape[0]:
        raise ValueError(
            f"Over 2.5 imputer feature mismatch: expected {medians_array.shape[0]}, got {values.shape[0]}"
        )
    return np.where(np.isnan(values), medians_array, values)


def _apply_scaler(values: np.ndarray, means: list[float], scales: list[float]) -> np.ndarray:
    means_array = np.asarray(means, dtype=float)
    scales_array = np.asarray(scales, dtype=float)
    if values.shape[0] != means_array.shape[0] or values.shape[0] != scales_array.shape[0]:
        raise ValueError("Over 2.5 scaler feature count does not match input features")
    safe_scales = np.where(scales_array == 0, 1, scales_array)
    return (values - means_array) / safe_scales


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
