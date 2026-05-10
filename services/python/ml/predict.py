"""Prediction helpers for the UFC Fight Predictor model."""
from __future__ import annotations

import math
from datetime import date
from pathlib import Path
from typing import Any

from xgboost import DMatrix
from xgboost import XGBClassifier

from ml.db import pool
from ml.features import FEATURE_NAMES, build_feature_row
from ml.train import REPO_ROOT


def predict_pair(fighter_a_id: str, fighter_b_id: str, fight_date: str) -> dict[str, Any]:
    """Predict a fight winner for the supplied fighter order and fight date."""
    parsed_date = date.fromisoformat(fight_date)
    model_row = _latest_model_version()
    model = XGBClassifier()
    model.load_model(REPO_ROOT / model_row["model_path"])

    features = build_feature_row(fighter_a_id, fighter_b_id, parsed_date)
    fighter_a_win_prob = float(model.predict_proba(features.reshape(1, -1))[0][1])
    contributing_features = _contributing_features(model, features)
    if fighter_a_win_prob >= 0.5:
        return {
            "predicted_winner_id": fighter_a_id,
            "win_prob": fighter_a_win_prob,
            "model_version": model_row["id"],
            "contributing_features": contributing_features,
        }
    return {
        "predicted_winner_id": fighter_b_id,
        "win_prob": 1.0 - fighter_a_win_prob,
        "model_version": model_row["id"],
        "contributing_features": contributing_features,
    }


def list_models(limit: int = 10) -> list[dict[str, Any]]:
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    trained_at,
                    training_set_size,
                    accuracy,
                    log_loss,
                    brier_score,
                    roc_auc,
                    model_path,
                    feature_importance
                FROM model_versions
                ORDER BY trained_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            return [_serialize_model_row(_row_dict(cur.description, row)) for row in cur.fetchall()]


def _latest_model_version() -> dict[str, Any]:
    models = list_models(1)
    if not models:
        raise RuntimeError("No trained model_versions rows found; run ml.train first")
    model_path = REPO_ROOT / models[0]["model_path"]
    if not model_path.exists():
        raise RuntimeError(f"Model file does not exist: {model_path}")
    return models[0]


def _contributing_features(model: XGBClassifier, features: Any, limit: int = 8) -> list[dict[str, Any]]:
    matrix = DMatrix(features.reshape(1, -1), feature_names=FEATURE_NAMES)
    contributions = model.get_booster().predict(matrix, pred_contribs=True)[0]
    ranked = sorted(
        zip(FEATURE_NAMES, features, contributions[:-1], strict=True),
        key=lambda item: abs(float(item[2])),
        reverse=True,
    )
    return [
        {
            "name": name,
            "value": _json_float(value),
            "shap": float(shap_value),
        }
        for name, value, shap_value in ranked[:limit]
    ]


def _json_float(value: Any) -> float | None:
    parsed = float(value)
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def _serialize_model_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "trained_at": row["trained_at"].isoformat(),
        "model_path": str(Path(row["model_path"])),
    }


def _row_dict(description: Any, row: Any) -> dict[str, Any]:
    return {column.name: value for column, value in zip(description, row, strict=True)}
