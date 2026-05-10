"""Train the first UFC Fight Predictor XGBoost model."""
from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from xgboost import XGBClassifier

from ml.db import pool
from ml.features import FEATURE_NAMES, build_features

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = REPO_ROOT / "data" / "models"


def train() -> dict[str, Any]:
    rows = _load_completed_fights()
    if len(rows) < 10:
        raise RuntimeError(f"Need at least 10 completed fights to train; found {len(rows)}")

    samples: list[tuple[datetime, np.ndarray, float]] = []
    for row in rows:
        features, label = build_features(row["fight_id"])
        if math.isnan(label):
            continue
        event_date = datetime.combine(row["event_date"], datetime.min.time(), tzinfo=UTC)
        samples.append((event_date, features, label))

    if len(samples) < 20:
        raise RuntimeError(f"Need at least 20 labeled samples to train; found {len(samples)}")

    samples.sort(key=lambda sample: sample[0])
    split_index = max(1, int(len(samples) * 0.8))
    if split_index >= len(samples):
        split_index = len(samples) - 1

    train_samples = samples[:split_index]
    holdout_samples = samples[split_index:]
    x_train = np.vstack([sample[1] for sample in train_samples])
    y_train = np.array([sample[2] for sample in train_samples], dtype=int)
    x_holdout = np.vstack([sample[1] for sample in holdout_samples])
    y_holdout = np.array([sample[2] for sample in holdout_samples], dtype=int)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        early_stopping_rounds=20,
        random_state=42,
    )
    model.fit(x_train, y_train, eval_set=[(x_holdout, y_holdout)], verbose=False)

    probabilities = model.predict_proba(x_holdout)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "log_loss": float(log_loss(y_holdout, probabilities, labels=[0, 1])),
        "brier_score": float(brier_score_loss(y_holdout, probabilities)),
        "accuracy": float(accuracy_score(y_holdout, predictions)),
        "roc_auc": _safe_roc_auc(y_holdout, probabilities),
    }

    model_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / f"{model_id}.json"
    model.save_model(model_path)

    top_features = _top_features(model)
    _insert_model_version(model_id, model_path, len(samples), metrics, top_features)

    return {
        "model_id": model_id,
        "model_path": str(model_path.relative_to(REPO_ROOT)),
        "training_set_size": len(samples),
        "train_rows": len(train_samples),
        "holdout_rows": len(holdout_samples),
        "top_features": top_features,
        **metrics,
    }


def _load_completed_fights() -> list[dict[str, Any]]:
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    f.id AS fight_id,
                    e.date AS event_date
                FROM fights f
                JOIN events e ON e.id = f.event_id
                JOIN fight_results fr ON fr.fight_id = f.id
                WHERE e.completed = true
                    AND fr.outcome IN ('win', 'loss')
                GROUP BY f.id, e.date
                HAVING count(*) = 2
                ORDER BY e.date, f.id
                """
            )
            return [_row_dict(cur.description, row) for row in cur.fetchall()]


def _insert_model_version(
    model_id: str,
    model_path: Path,
    training_set_size: int,
    metrics: dict[str, float],
    top_features: list[dict[str, float | str]],
) -> None:
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO model_versions (
                    id,
                    trained_at,
                    training_set_size,
                    accuracy,
                    log_loss,
                    brier_score,
                    roc_auc,
                    model_path,
                    feature_importance
                )
                VALUES (%s, now(), %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    model_id,
                    training_set_size,
                    metrics["accuracy"],
                    metrics["log_loss"],
                    metrics["brier_score"],
                    metrics["roc_auc"],
                    str(model_path.relative_to(REPO_ROOT)),
                    json.dumps(top_features),
                ),
            )
        conn.commit()


def _top_features(model: XGBClassifier) -> list[dict[str, float | str]]:
    importances = getattr(model, "feature_importances_", np.zeros(len(FEATURE_NAMES)))
    ranked = sorted(
        zip(FEATURE_NAMES, importances, strict=True),
        key=lambda item: float(item[1]),
        reverse=True,
    )
    return [
        {"name": name, "importance": float(importance)}
        for name, importance in ranked[:8]
        if float(importance) > 0
    ]


def _safe_roc_auc(y_true: np.ndarray, probabilities: np.ndarray) -> float:
    try:
        return float(roc_auc_score(y_true, probabilities))
    except ValueError:
        return math.nan


def _row_dict(description: Any, row: Any) -> dict[str, Any]:
    return {column.name: value for column, value in zip(description, row, strict=True)}


def main() -> None:
    print(json.dumps(train(), allow_nan=True))


if __name__ == "__main__":
    main()
