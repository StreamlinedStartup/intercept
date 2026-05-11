"""Report-only offline experiments for UFC Fight Predictor feature variants."""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np

from ml.backtest import (
    _confidence_bucket,
    _fit_model,
    _grouped_metrics,
    _load_completed_fights,
    _metrics,
    _predict_sample,
    _target_events,
)
from ml.features import (
    EXPERIMENT_FEATURE_NAMES,
    FEATURE_NAMES,
    WEIGHT_CLASS_RECORD_FEATURE_NAMES,
    build_features,
)
from ml.train import REPO_ROOT

DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "experiments"

RECENT_FORM_FEATURES = {
    "wins_last_3_diff",
    "wins_last_5_diff",
    "loss_streak_a",
    "loss_streak_b",
    "coming_off_loss_a",
    "coming_off_loss_b",
    "days_since_last_fight_a",
    "days_since_last_fight_b",
    "days_since_last_fight_diff",
    "long_layoff_a",
    "long_layoff_b",
}
DAMAGE_FEATURES = {"damage_index_a", "damage_index_b"}
COMMON_OPPONENT_FEATURES = {"common_opponent_count", "common_opponent_win_diff"}
STANCE_FEATURES = {
    "stance_orthodox_orthodox",
    "stance_orthodox_southpaw",
    "stance_southpaw_orthodox",
    "stance_southpaw_southpaw",
    "stance_switch_involved",
    "stance_unknown",
}
PHYSICAL_FEATURES = {"height_diff", "reach_diff", "age_diff"}
CAREER_STAT_FEATURES = {
    "slpm_diff",
    "str_acc_diff",
    "sapm_diff",
    "str_def_diff",
    "td_avg_diff",
    "td_acc_diff",
    "td_def_diff",
    "sub_avg_diff",
    "finish_rate_diff",
    "decision_rate_diff",
    "time_in_cage_a",
    "time_in_cage_b",
    "avg_ending_round_diff",
    "decision_tendency_diff",
    "late_round_exposure_diff",
}
WEIGHT_CLASS_BASELINE_FEATURES = {"weight_class_change", "same_weight_class_count_diff"}


@dataclass(frozen=True)
class FeatureVariant:
    name: str
    description: str
    feature_names: list[str]


def feature_variants() -> list[FeatureVariant]:
    baseline = list(FEATURE_NAMES)
    return [
        FeatureVariant("baseline", "Current production feature set.", baseline),
        FeatureVariant(
            "no_weight_class",
            "Baseline with existing weight-class movement features removed.",
            _without(baseline, WEIGHT_CLASS_BASELINE_FEATURES),
        ),
        FeatureVariant(
            "weight_class_record_v1",
            "Baseline plus division-specific prior record and pound-move features.",
            [*baseline, *WEIGHT_CLASS_RECORD_FEATURE_NAMES],
        ),
        FeatureVariant(
            "no_recent_form",
            "Baseline without recent-form features.",
            _without(baseline, RECENT_FORM_FEATURES),
        ),
        FeatureVariant("no_damage", "Baseline without damage proxy features.", _without(baseline, DAMAGE_FEATURES)),
        FeatureVariant(
            "no_common_opponents",
            "Baseline without common-opponent features.",
            _without(baseline, COMMON_OPPONENT_FEATURES),
        ),
        FeatureVariant("no_stance", "Baseline without stance interaction features.", _without(baseline, STANCE_FEATURES)),
        FeatureVariant("no_physical", "Baseline without height, reach, and age.", _without(baseline, PHYSICAL_FEATURES)),
        FeatureVariant(
            "no_career_stats",
            "Baseline without career statistical profile features.",
            _without(baseline, CAREER_STAT_FEATURES),
        ),
    ]


def run_feature_variant_experiment(
    *,
    min_train_samples: int,
    screen_start_date: date,
    screen_max_events: int,
    full_finalists: int,
    end_date: date | None,
    output_path: Path,
    markdown_path: Path,
    progress_every: int | None = None,
) -> dict[str, Any]:
    variants = feature_variants()
    samples = _build_experiment_samples(end_date)
    screen_results = [
        _run_variant_stage(
            variant,
            samples=samples,
            stage="screen",
            start_date=screen_start_date,
            end_date=end_date,
            max_events=screen_max_events,
            min_train_samples=min_train_samples,
            progress_every=progress_every,
        )
        for variant in variants
    ]
    ranked_screen = rank_variant_results(screen_results)
    finalist_names = [row["variant"] for row in ranked_screen[:full_finalists]]
    finalist_variants = [variant for variant in variants if variant.name in finalist_names]
    full_results = [
        _run_variant_stage(
            variant,
            samples=samples,
            stage="full",
            start_date=screen_start_date,
            end_date=end_date,
            max_events=None,
            min_train_samples=min_train_samples,
            progress_every=progress_every,
        )
        for variant in finalist_variants
    ]
    ranked_full = rank_variant_results(full_results)
    report = _build_report(
        variants=variants,
        screen_results=screen_results,
        full_results=full_results,
        ranked_screen=ranked_screen,
        ranked_full=ranked_full,
        finalist_names=finalist_names,
        args={
            "min_train_samples": min_train_samples,
            "screen_start_date": screen_start_date.isoformat(),
            "screen_max_events": screen_max_events,
            "full_finalists": full_finalists,
            "end_date": end_date.isoformat() if end_date else None,
            "output": _display_path(output_path),
            "markdown": _display_path(markdown_path),
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(_markdown_report(report) + "\n")
    return report


def rank_variant_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(results, key=_ranking_key)


def _without(feature_names: list[str], excluded: set[str]) -> list[str]:
    return [name for name in feature_names if name not in excluded]


def _run_variant_stage(
    variant: FeatureVariant,
    *,
    samples: list[dict[str, Any]],
    stage: str,
    start_date: date,
    end_date: date | None,
    max_events: int | None,
    min_train_samples: int,
    progress_every: int | None,
) -> dict[str, Any]:
    report = _run_projected_backtest(
        samples=_project_samples(samples, variant.feature_names),
        start_date=start_date,
        end_date=end_date,
        max_events=max_events,
        min_train_samples=min_train_samples,
        progress_every=progress_every,
        feature_names=variant.feature_names,
    )
    return {
        "variant": variant.name,
        "stage": stage,
        "events_scored": report["events_scored"],
        "predictions_scored": report["predictions_scored"],
        "feature_count": len(variant.feature_names),
        "overall": report["overall"],
        "by_confidence_bucket": report["by_confidence_bucket"],
    }


def _build_experiment_samples(end_date: date | None) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _load_completed_fights()
        if end_date is None or row["event_date"] <= end_date
    ]
    samples = []
    for row in rows:
        features, label = build_features(row["fight_id"], feature_names=EXPERIMENT_FEATURE_NAMES)
        if math.isnan(label):
            continue
        samples.append({**row, "features": features, "label": int(label)})
    return samples


def _project_samples(
    samples: list[dict[str, Any]],
    feature_names: list[str],
) -> list[dict[str, Any]]:
    index_by_name = {name: index for index, name in enumerate(EXPERIMENT_FEATURE_NAMES)}
    indices = [index_by_name[name] for name in feature_names]
    return [{**sample, "features": np.asarray(sample["features"])[indices]} for sample in samples]


def _run_projected_backtest(
    *,
    samples: list[dict[str, Any]],
    start_date: date,
    end_date: date | None,
    max_events: int | None,
    min_train_samples: int,
    progress_every: int | None,
    feature_names: list[str],
) -> dict[str, Any]:
    events = _target_events(samples, start_date, end_date)
    predictions: list[dict[str, Any]] = []
    event_reports: list[dict[str, Any]] = []
    for index, event in enumerate(events, start=1):
        train_samples = [sample for sample in samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in samples if sample["event_id"] == event["event_id"]]
        if len(train_samples) < min_train_samples or not target_samples:
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
        if progress_every and len(event_reports) % progress_every == 0:
            print(
                f"{event['event_date'].isoformat()} {_stage_progress(feature_names, len(event_reports))}",
                file=sys.stderr,
                flush=True,
            )
        if max_events is not None and len(event_reports) >= max_events:
            break
    return {
        "feature_names": feature_names,
        "events_scored": len(event_reports),
        "predictions_scored": len(predictions),
        "overall": _metrics(predictions),
        "by_confidence_bucket": _grouped_metrics(
            predictions,
            lambda row: _confidence_bucket(row["confidence"]),
        ),
    }


def _stage_progress(feature_names: list[str], events_scored: int) -> str:
    return f"{len(feature_names)} features, {events_scored} events scored"


def _build_report(
    *,
    variants: list[FeatureVariant],
    screen_results: list[dict[str, Any]],
    full_results: list[dict[str, Any]],
    ranked_screen: list[dict[str, Any]],
    ranked_full: list[dict[str, Any]],
    finalist_names: list[str],
    args: dict[str, Any],
) -> dict[str, Any]:
    screen_baseline = _find_result(screen_results, "baseline")
    full_baseline = _find_result(full_results, "baseline") or screen_baseline
    stage_for_delta = full_results if full_results else screen_results
    baseline_for_delta = _find_result(stage_for_delta, "baseline") or full_baseline
    annotated_screen = _annotate_results(screen_results, screen_baseline)
    annotated_full = _annotate_results(full_results, baseline_for_delta)
    winner = (ranked_full or ranked_screen)[0] if (ranked_full or ranked_screen) else None
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "experiment": "feature-variants",
        "args": args,
        "variant_definitions": [
            {
                "name": variant.name,
                "description": variant.description,
                "feature_count": len(variant.feature_names),
                "feature_names": variant.feature_names,
            }
            for variant in variants
        ],
        "ranking_rules": [
            "lower log_loss",
            "lower brier_score",
            "lower abs_calibration_error",
            "higher roc_auc",
            "higher accuracy",
        ],
        "screen_results": annotated_screen,
        "ranked_screen": [row["variant"] for row in ranked_screen],
        "finalists": finalist_names,
        "full_results": annotated_full,
        "ranked_full": [row["variant"] for row in ranked_full],
        "winner": winner["variant"] if winner else None,
        "recommended_next_action": _recommended_next_action(winner, full_baseline or screen_baseline),
    }


def _annotate_results(
    results: list[dict[str, Any]],
    baseline: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if baseline is None:
        return results
    baseline_overconfidence = _bucket_overconfidence(baseline, "70+")
    annotated = []
    for result in results:
        overconfidence = _bucket_overconfidence(result, "70+")
        annotated.append(
            {
                **result,
                "delta_vs_baseline": _metric_deltas(result["overall"], baseline["overall"]),
                "confidence_70_plus": result["by_confidence_bucket"].get("70+"),
                "overconfident_70_plus_vs_baseline": (
                    overconfidence is not None
                    and baseline_overconfidence is not None
                    and overconfidence - baseline_overconfidence >= 0.02
                ),
            }
        )
    return annotated


def _metric_deltas(metrics: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    deltas = {}
    for name in ["log_loss", "brier_score", "abs_calibration_error", "roc_auc", "accuracy"]:
        value = metrics.get(name)
        base = baseline.get(name)
        deltas[name] = None if value is None or base is None else value - base
    return deltas


def _bucket_overconfidence(result: dict[str, Any], bucket: str) -> float | None:
    metrics = result["by_confidence_bucket"].get(bucket)
    if metrics is None or metrics.get("calibration_gap") is None:
        return None
    return max(0.0, -float(metrics["calibration_gap"]))


def _find_result(results: list[dict[str, Any]], variant_name: str) -> dict[str, Any] | None:
    return next((result for result in results if result["variant"] == variant_name), None)


def _ranking_key(result: dict[str, Any]) -> tuple[float, float, float, float, float]:
    metrics = result["overall"]
    return (
        _low(metrics.get("log_loss")),
        _low(metrics.get("brier_score")),
        _low(metrics.get("abs_calibration_error")),
        _high(metrics.get("roc_auc")),
        _high(metrics.get("accuracy")),
    )


def _low(value: Any) -> float:
    if value is None or math.isnan(float(value)):
        return math.inf
    return float(value)


def _high(value: Any) -> float:
    if value is None or math.isnan(float(value)):
        return math.inf
    return -float(value)


def _recommended_next_action(
    winner: dict[str, Any] | None,
    baseline: dict[str, Any] | None,
) -> str:
    if winner is None or baseline is None:
        return "Rerun after enough completed fights are available for comparison."
    if winner["variant"] == "baseline":
        return "Keep the production feature set and use the report as baseline evidence."
    deltas = _metric_deltas(winner["overall"], baseline["overall"])
    if (
        deltas["log_loss"] is not None
        and deltas["log_loss"] < 0
        and not winner.get("overconfident_70_plus_vs_baseline")
    ):
        return f"Investigate {winner['variant']} as a candidate feature-set change; do not promote automatically."
    return f"Keep {winner['variant']} as research evidence only; probability quality is not cleanly better than baseline."


def _markdown_report(report: dict[str, Any]) -> str:
    full_results = report["full_results"] or report["screen_results"]
    ranked_names = report["ranked_full"] or report["ranked_screen"]
    ranked = [
        next(row for row in full_results if row["variant"] == name)
        for name in ranked_names
    ]
    baseline = next((row for row in full_results if row["variant"] == "baseline"), None)
    winner = ranked[0] if ranked else None
    lines = [
        "# Feature-Variant Experiment",
        "",
        f"Generated: {report['generated_at']}",
        f"Winner: {report['winner'] or 'none'}",
        f"Recommended next action: {report['recommended_next_action']}",
        "",
        "## Ranked Summary",
        "",
        "| Rank | Variant | Events | Predictions | Log loss | Brier | Abs calib err | ROC AUC | Accuracy | 70%+ count | 70%+ accuracy | 70%+ gap | Flag |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for rank, result in enumerate(ranked, start=1):
        high_bucket = result.get("confidence_70_plus") or {}
        lines.append(
            "| "
            f"{rank} | {result['variant']} | {result['events_scored']} | {result['predictions_scored']} | "
            f"{_fmt(result['overall'].get('log_loss'))} | {_fmt(result['overall'].get('brier_score'))} | "
            f"{_fmt(result['overall'].get('abs_calibration_error'))} | {_fmt(result['overall'].get('roc_auc'))} | "
            f"{_fmt(result['overall'].get('accuracy'))} | {high_bucket.get('count', 0)} | "
            f"{_fmt(high_bucket.get('accuracy'))} | {_fmt(high_bucket.get('calibration_gap'))} | "
            f"{'70%+ overconfident' if result.get('overconfident_70_plus_vs_baseline') else ''} |"
        )
    lines.extend(["", "## Baseline vs Winner", ""])
    if baseline and winner:
        lines.extend(
            [
                "| Metric | Baseline | Winner | Delta |",
                "|---|---:|---:|---:|",
            ]
        )
        for name in ["log_loss", "brier_score", "abs_calibration_error", "roc_auc", "accuracy"]:
            lines.append(
                f"| {name} | {_fmt(baseline['overall'].get(name))} | {_fmt(winner['overall'].get(name))} | "
                f"{_fmt(winner.get('delta_vs_baseline', {}).get(name))} |"
            )
    lines.extend(["", "## 70%+ Bucket", ""])
    lines.extend(
        [
            "| Variant | Count | Accuracy | Avg confidence | Calibration gap | Abs calib err |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for result in ranked:
        bucket = result.get("confidence_70_plus") or {}
        lines.append(
            f"| {result['variant']} | {bucket.get('count', 0)} | {_fmt(bucket.get('accuracy'))} | "
            f"{_fmt(bucket.get('avg_confidence'))} | {_fmt(bucket.get('calibration_gap'))} | "
            f"{_fmt(bucket.get('abs_calibration_error'))} |"
        )
    return "\n".join(lines)


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.4f}"
    return str(value)


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run offline UFC predictor experiments")
    subparsers = parser.add_subparsers(dest="command", required=True)
    feature_parser = subparsers.add_parser("feature-variants")
    feature_parser.add_argument("--min-train-samples", type=int, default=200)
    feature_parser.add_argument("--screen-start-date", type=date.fromisoformat, required=True)
    feature_parser.add_argument("--screen-max-events", type=int, default=120)
    feature_parser.add_argument("--full-finalists", type=int, default=5)
    feature_parser.add_argument("--end-date", type=date.fromisoformat, default=None)
    feature_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR / "feature-variants.json")
    feature_parser.add_argument("--markdown", type=Path, default=DEFAULT_OUTPUT_DIR / "feature-variants.md")
    feature_parser.add_argument("--progress-every", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.command == "feature-variants":
        report = run_feature_variant_experiment(
            min_train_samples=args.min_train_samples,
            screen_start_date=args.screen_start_date,
            screen_max_events=args.screen_max_events,
            full_finalists=args.full_finalists,
            end_date=args.end_date,
            output_path=_resolve_repo_path(args.output),
            markdown_path=_resolve_repo_path(args.markdown),
            progress_every=args.progress_every,
        )
        print(
            json.dumps(
                {
                    "output": report["args"]["output"],
                    "markdown": report["args"]["markdown"],
                    "winner": report["winner"],
                    "ranked_full": report["ranked_full"],
                    "ranked_screen": report["ranked_screen"],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
