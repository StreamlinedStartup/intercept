"""Report-only market baseline and blend gate for UFC Fight Predictor."""
from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score

from ml.odds_aware_report import (
    flat_stake_net_profit,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-gate-report.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-gate-report.md"

VALIDATION_MIN_FIGHTS = 200
VALIDATION_MIN_MARKET_EVENTS = 30
VALIDATION_MIN_MARKET_ROI_DELTA = 0.02


def run_market_gate_report(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
    min_train_samples: int = 200,
) -> dict[str, Any]:
    from ml.baselines import _load_market_consensus
    from ml.odds_aware_report import _load_source_coverage

    del min_train_samples
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    markets = _load_market_consensus()
    strategies = [
        _strategy_report("model_pick", "Leak-free UFC experience baseline pick", samples, markets, model_weight=1.0),
        _strategy_report("market_favorite", "No-vig market favorite", samples, markets, model_weight=0.0),
        _strategy_report("blend_50_50", "50% model baseline probability + 50% market probability", samples, markets, model_weight=0.5),
        _strategy_report("blend_25_model_75_market", "25% model baseline probability + 75% market probability", samples, markets, model_weight=0.25),
        _strategy_report("blend_75_model_25_market", "75% model baseline probability + 25% market probability", samples, markets, model_weight=0.75),
    ]
    gate = _validation_gate({"summary": _scored_summary(coverage, samples)}, strategies)
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-gate-report",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": gate["value_status"],
        "value_status_reason": gate["value_status_reason"],
        "validation_thresholds": {
            "min_fights": VALIDATION_MIN_FIGHTS,
            "min_market_events": VALIDATION_MIN_MARKET_EVENTS,
            "min_market_roi_delta": VALIDATION_MIN_MARKET_ROI_DELTA,
        },
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
        },
        "timestamp_semantics": {
            "label": (
                "FightOdds source_current lines are captured at import scrape time. "
                "This report uses them as current/consensus market probabilities only, not as true closing-line value."
            ),
            "closing_line_value": "not_available_without_timestamped_or_open_close_lines",
        },
        "strategies": strategies,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    lines = [
        "# Market Gate Report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Reason: {report['value_status_reason']}",
        f"- Scored events: {coverage['scored_events']}",
        f"- Scored fights: {coverage['scored_fights']}",
        f"- Moneyline rows linked: {coverage['moneyline_rows_linked']}/{coverage['moneyline_rows_imported']}",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        "",
        "## Strategy Comparison",
        "",
        "| Strategy | Count | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC | Sim ROI |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy in report["strategies"]:
        metrics = strategy["metrics"]
        roi = strategy["simulated_research_roi"]
        lines.append(
            "| {name} | {count} | {accuracy} | {avg_confidence} | {calibration_gap} | {log_loss} | {brier} | {roc_auc} | {roi} |".format(
                name=strategy["name"],
                count=metrics["count"],
                accuracy=_fmt_pct(metrics["accuracy"]),
                avg_confidence=_fmt_pct(metrics["avg_confidence"]),
                calibration_gap=_fmt_signed_pct(metrics["calibration_gap"]),
                log_loss=_fmt_metric(metrics["log_loss"]),
                brier=_fmt_metric(metrics["brier_score"]),
                roc_auc=_fmt_metric(metrics["roc_auc"]),
                roi=_fmt_pct(roi["roi_pct"]),
            )
        )
    lines.extend(
        [
            "",
            "## Timestamp Semantics",
            "",
            report["timestamp_semantics"]["label"],
            "",
            "## Policy",
            "",
            "This report is a market gate, not a promotion. A validated value status requires enough matched market history and a durable improvement over the market baseline.",
        ]
    )
    return "\n".join(lines)


def _strategy_report(
    name: str,
    description: str,
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
    *,
    model_weight: float,
) -> dict[str, Any]:
    predictions = [_prediction_for_sample(sample, markets, model_weight) for sample in samples]
    return {
        "name": name,
        "description": description,
        "model_weight": model_weight,
        "market_weight": 1 - model_weight,
        "metrics": _metrics(predictions),
        "simulated_research_roi": _roi(predictions),
    }


def _prediction_for_sample(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    model_weight: float,
) -> dict[str, Any]:
    from ml.baselines import _ufc_experience_probability

    market = markets[sample["fight_id"]]
    model_probability = _ufc_experience_probability(sample)
    market_probability = market[sample["fighter_a_id"]]["market_prob"]
    fighter_a_probability = (
        model_weight * model_probability
        + (1 - model_weight) * market_probability
    )
    predicted_label = 1 if fighter_a_probability >= 0.5 else 0
    picked_fighter_id = sample["fighter_a_id"] if predicted_label == 1 else sample["fighter_b_id"]
    pick_market = market[picked_fighter_id]
    won = predicted_label == sample["label"]
    return {
        "fight_id": sample["fight_id"],
        "event_id": sample["event_id"],
        "fighter_a_probability": fighter_a_probability,
        "actual_label": sample["label"],
        "predicted_label": predicted_label,
        "confidence": fighter_a_probability if predicted_label == 1 else 1 - fighter_a_probability,
        "won": won,
        "decimal_odds": pick_market["decimal_odds"],
        "net_profit": flat_stake_net_profit(pick_market["decimal_odds"], won),
    }


def _metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        return {
            "count": 0,
            "accuracy": None,
            "avg_confidence": None,
            "calibration_gap": None,
            "abs_calibration_error": None,
            "log_loss": None,
            "brier_score": None,
            "roc_auc": None,
        }
    y_true = np.array([row["actual_label"] for row in predictions], dtype=int)
    probabilities = np.array([row["fighter_a_probability"] for row in predictions], dtype=float)
    predicted = np.array([row["predicted_label"] for row in predictions], dtype=int)
    confidence = np.array([row["confidence"] for row in predictions], dtype=float)
    accuracy = float(accuracy_score(y_true, predicted))
    avg_confidence = float(np.mean(confidence))
    return {
        "count": len(predictions),
        "accuracy": accuracy,
        "avg_confidence": avg_confidence,
        "calibration_gap": accuracy - avg_confidence,
        "abs_calibration_error": abs(accuracy - avg_confidence),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1])),
        "brier_score": float(brier_score_loss(y_true, probabilities)),
        "roc_auc": _safe_roc_auc(y_true, probabilities),
    }


def _roi(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    units = sum(float(row["net_profit"]) for row in predictions)
    return {
        "entries": len(predictions),
        "wins": sum(1 for row in predictions if row["won"]),
        "units": units,
        "roi_pct": units / len(predictions) if predictions else None,
        "stake_unit": "flat_1u",
        "status": "simulated_research_only",
    }


def _validation_gate(odds_report: dict[str, Any], strategies: list[dict[str, Any]]) -> dict[str, str]:
    scored_fights = int(odds_report["summary"]["scored_fights"])
    scored_events = int(odds_report["summary"]["scored_events"])
    model = next(strategy for strategy in strategies if strategy["name"] == "model_pick")
    market = next(strategy for strategy in strategies if strategy["name"] == "market_favorite")
    model_roi = model["simulated_research_roi"]["roi_pct"]
    market_roi = market["simulated_research_roi"]["roi_pct"]
    if scored_fights < VALIDATION_MIN_FIGHTS or scored_events < VALIDATION_MIN_MARKET_EVENTS:
        return {
            "value_status": "insufficient_coverage",
            "value_status_reason": (
                f"Only {scored_fights} matched fights across {scored_events} events were scored; "
                f"need at least {VALIDATION_MIN_FIGHTS} fights across {VALIDATION_MIN_MARKET_EVENTS} events."
            ),
        }
    if model_roi is None or market_roi is None or model_roi < market_roi + VALIDATION_MIN_MARKET_ROI_DELTA:
        return {
            "value_status": "research_only",
            "value_status_reason": "Model ROI did not clear the market-favorite baseline gate.",
        }
    return {
        "value_status": "validated",
        "value_status_reason": "Model cleared configured coverage and market baseline gates.",
        }


def _load_matched_market_samples(coverage: dict[str, Any]) -> list[dict[str, Any]]:
    from ml.baselines import _load_market_consensus, _load_samples

    matched_events = [
        event for event in coverage["events"]
        if event["match_status"] == "matched" and event["canonical_event_id"] is not None
    ]
    if not matched_events:
        return []
    event_ids = {event["canonical_event_id"] for event in matched_events}
    dates = [datetime.fromisoformat(event["event_date"]).date() for event in matched_events]
    samples, _events = _load_samples(
        start_date=min(dates),
        end_date=max(dates),
        max_events=None,
    )
    markets = _load_market_consensus()
    return [
        sample for sample in samples
        if sample["event_id"] in event_ids
        and sample["fight_id"] in markets
        and sample["fighter_a_id"] in markets[sample["fight_id"]]
        and sample["fighter_b_id"] in markets[sample["fight_id"]]
    ]


def _scored_summary(coverage: dict[str, Any], samples: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        **coverage["summary"],
        "scored_events": len({sample["event_id"] for sample in samples}),
        "scored_fights": len(samples),
    }


def _safe_roc_auc(y_true: np.ndarray, probabilities: np.ndarray) -> float | None:
    try:
        value = float(roc_auc_score(y_true, probabilities))
    except ValueError:
        return None
    return None if math.isnan(value) else value


def _fmt_metric(value: Any) -> str:
    return "" if value is None else f"{float(value):.4f}"


def _fmt_pct(value: Any) -> str:
    return "" if value is None else f"{float(value) * 100:.1f}%"


def _fmt_signed_pct(value: Any) -> str:
    return "" if value is None else f"{float(value) * 100:+.1f}%"


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the market baseline and blend gate report")
    parser.add_argument("--min-train-samples", type=int, default=200)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_market_gate_report(
        output_path=output_path,
        markdown_path=markdown_path,
        min_train_samples=args.min_train_samples,
    )
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "value_status": report["value_status"],
        "coverage": report["coverage"],
        "strategies": [
            {
                "name": strategy["name"],
                "metrics": strategy["metrics"],
                "simulated_research_roi": strategy["simulated_research_roi"],
            }
            for strategy in report["strategies"]
        ],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
