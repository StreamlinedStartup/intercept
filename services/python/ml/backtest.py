"""Walk-forward backtesting for UFC Fight Predictor models."""
from __future__ import annotations

import argparse
import json
import math
import sys
import warnings
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from xgboost import XGBClassifier

from ml.db import pool
from ml.features import FEATURE_NAMES, build_features
from ml.train import REPO_ROOT

DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "backtests"


def run_walk_forward_backtest(
    *,
    start_date: date | None = None,
    max_events: int | None = None,
    min_train_samples: int = 200,
    output_path: Path | None = None,
    progress_every: int | None = None,
) -> dict[str, Any]:
    """Train on fights before each event and predict that event."""
    completed_fights = _load_completed_fights()
    samples = _build_samples(completed_fights)
    events = _target_events(samples, start_date)
    predictions: list[dict[str, Any]] = []
    event_reports: list[dict[str, Any]] = []

    for index, event in enumerate(events, start=1):
        train_samples = [sample for sample in samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
            _print_progress(
                progress_every,
                index,
                len(events),
                event,
                len(event_reports),
                len(predictions),
                "skipped",
            )
            continue

        model = _fit_model(train_samples)
        event_predictions = [_predict_sample(model, sample) for sample in target_samples]
        predictions.extend(event_predictions)
        event_reports.append(
            {
                "event_id": event["event_id"],
                "event_name": event["event_name"],
                "event_date": event["event_date"].isoformat(),
                "train_samples": len(train_samples),
                "predictions": len(event_predictions),
                **_metrics(event_predictions),
            }
        )

        _print_progress(
            progress_every,
            index,
            len(events),
            event,
            len(event_reports),
            len(predictions),
            "scored",
        )

        if max_events is not None and len(event_reports) >= max_events:
            break

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "start_date": start_date.isoformat() if start_date else None,
        "max_events": max_events,
        "min_train_samples": min_train_samples,
        "feature_names": FEATURE_NAMES,
        "events_scored": len(event_reports),
        "predictions_scored": len(predictions),
        "overall": _metrics(predictions),
        "by_month": _grouped_metrics(predictions, lambda row: row["event_date"][:7]),
        "by_confidence_bucket": _grouped_metrics(
            predictions,
            lambda row: _confidence_bucket(row["confidence"]),
        ),
        "by_model_edge_bucket": _grouped_metrics(
            predictions,
            lambda row: _edge_bucket(row["model_edge"]),
        ),
        "events": event_reports,
    }

    destination = output_path or _default_output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    report["output_path"] = str(destination.relative_to(REPO_ROOT))
    return report


def _load_completed_fights() -> list[dict[str, Any]]:
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    f.id AS fight_id,
                    f.event_id,
                    f.weight_class,
                    e.name AS event_name,
                    e.date AS event_date
                FROM fights f
                JOIN events e ON e.id = f.event_id
                JOIN fight_results fr ON fr.fight_id = f.id
                WHERE e.completed = true
                    AND e.promotion = 'ufc'
                    AND fr.outcome IN ('win', 'loss')
                GROUP BY f.id, f.event_id, f.weight_class, e.name, e.date
                HAVING count(*) = 2
                ORDER BY e.date, f.id
                """
            )
            return [_row_dict(cur.description, row) for row in cur.fetchall()]


def _build_samples(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for row in rows:
        features, label = build_features(row["fight_id"])
        if math.isnan(label):
            continue
        samples.append(
            {
                **row,
                "features": features,
                "label": int(label),
            }
        )
    return samples


def _target_events(samples: list[dict[str, Any]], start_date: date | None) -> list[dict[str, Any]]:
    events_by_id: dict[str, dict[str, Any]] = {}
    for sample in samples:
        if start_date is not None and sample["event_date"] < start_date:
            continue
        events_by_id[sample["event_id"]] = {
            "event_id": sample["event_id"],
            "event_name": sample["event_name"],
            "event_date": sample["event_date"],
        }
    return sorted(events_by_id.values(), key=lambda row: (row["event_date"], row["event_id"]))


def _fit_model(samples: list[dict[str, Any]]) -> XGBClassifier:
    x_train = np.vstack([sample["features"] for sample in samples])
    y_train = np.array([sample["label"] for sample in samples], dtype=int)
    model = XGBClassifier(
        n_estimators=80,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(x_train, y_train, verbose=False)
    return model


def _predict_sample(model: XGBClassifier, sample: dict[str, Any]) -> dict[str, Any]:
    probability = float(model.predict_proba(sample["features"].reshape(1, -1))[0][1])
    predicted_label = 1 if probability >= 0.5 else 0
    confidence = probability if predicted_label == 1 else 1.0 - probability
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "event_date": sample["event_date"].isoformat(),
        "predicted_label": predicted_label,
        "actual_label": sample["label"],
        "fighter_a_win_prob": probability,
        "confidence": confidence,
        "model_edge": confidence - 0.5,
        "correct": predicted_label == sample["label"],
    }


def _metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        return {
            "count": 0,
            "accuracy": None,
            "log_loss": None,
            "brier_score": None,
            "roc_auc": None,
        }

    y_true = np.array([row["actual_label"] for row in predictions], dtype=int)
    probabilities = np.array([row["fighter_a_win_prob"] for row in predictions], dtype=float)
    predicted = np.array([row["predicted_label"] for row in predictions], dtype=int)
    return {
        "count": len(predictions),
        "accuracy": float(accuracy_score(y_true, predicted)),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1])),
        "brier_score": float(brier_score_loss(y_true, probabilities)),
        "roc_auc": _safe_roc_auc(y_true, probabilities),
    }


def _grouped_metrics(
    predictions: list[dict[str, Any]],
    key_fn: Any,
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in predictions:
        grouped[key_fn(row)].append(row)
    return {key: _metrics(rows) for key, rows in sorted(grouped.items())}


def _confidence_bucket(confidence: float) -> str:
    if confidence < 0.55:
        return "50-55"
    if confidence < 0.60:
        return "55-60"
    if confidence < 0.65:
        return "60-65"
    if confidence < 0.70:
        return "65-70"
    return "70+"


def _edge_bucket(edge: float) -> str:
    if edge < 0.02:
        return "0-2"
    if edge < 0.05:
        return "2-5"
    if edge < 0.10:
        return "5-10"
    return "10+"


def _safe_roc_auc(y_true: np.ndarray, probabilities: np.ndarray) -> float | None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", UndefinedMetricWarning)
        try:
            value = float(roc_auc_score(y_true, probabilities))
        except (UndefinedMetricWarning, ValueError):
            return None
    if math.isnan(value):
        return None
    return value


def _print_progress(
    progress_every: int | None,
    event_index: int,
    event_count: int,
    event: dict[str, Any],
    events_scored: int,
    predictions_scored: int,
    status: str,
) -> None:
    if progress_every is None or progress_every <= 0:
        return
    if event_index != 1 and event_index % progress_every != 0 and event_index != event_count:
        return
    print(
        "backtest progress: "
        f"{event_index}/{event_count} candidates, "
        f"{events_scored} events scored, "
        f"{predictions_scored} predictions, "
        f"{status} {event['event_date'].isoformat()} {event['event_name']}",
        file=sys.stderr,
        flush=True,
    )


def _default_output_path() -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return DEFAULT_OUTPUT_DIR / f"walk-forward-{stamp}.json"


def _row_dict(description: Any, row: Any) -> dict[str, Any]:
    return {column.name: value for column, value in zip(description, row, strict=True)}


def _cli_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "output_path": report.get("output_path"),
        "start_date": report.get("start_date"),
        "max_events": report.get("max_events"),
        "min_train_samples": report.get("min_train_samples"),
        "events_scored": report.get("events_scored"),
        "predictions_scored": report.get("predictions_scored"),
        "overall": report.get("overall"),
        "by_confidence_bucket": report.get("by_confidence_bucket"),
        "by_model_edge_bucket": report.get("by_model_edge_bucket"),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a UFC Fight Predictor walk-forward backtest")
    parser.add_argument("--start-date", type=date.fromisoformat, default=None)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--min-train-samples", type=int, default=200)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--progress-every",
        type=int,
        default=None,
        help="Print progress to stderr every N candidate events.",
    )
    parser.add_argument(
        "--stdout",
        choices=["summary", "full", "none"],
        default="summary",
        help="Control the JSON printed after writing the report.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = args.output
    if output_path is not None and not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    report = run_walk_forward_backtest(
        start_date=args.start_date,
        max_events=args.max_events,
        min_train_samples=args.min_train_samples,
        output_path=output_path,
        progress_every=args.progress_every,
    )
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else _cli_summary(report)
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
