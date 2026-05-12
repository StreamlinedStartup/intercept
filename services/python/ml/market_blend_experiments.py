"""Report-only market-aware calibration and blend experiments."""
from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ml.baselines import _load_market_consensus, _ufc_experience_probability
from ml.market_gate_report import _load_matched_market_samples, _metrics, _roi
from ml.odds_aware_report import _load_source_coverage, flat_stake_net_profit

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "experiments" / "market-aware-blend-experiments.json"
DEFAULT_MARKDOWN = REPO_ROOT / "data" / "experiments" / "market-aware-blend-experiments.md"
MIN_MARKET_ROI_DELTA = 0.02


type ProbabilityFn = Callable[[float, float], float]


def run_market_blend_experiments(
    *,
    output_path: Path = DEFAULT_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> dict[str, Any]:
    coverage = _load_source_coverage()
    samples = _load_matched_market_samples(coverage)
    markets = _load_market_consensus()
    variants = [
        _variant("market_favorite", "No-vig market favorite baseline", "baseline", lambda model, market: market),
        _variant("model_pick", "Current leak-free UFC experience model pick", "model", lambda model, market: model),
        *[
            _variant(
                f"blend_{_pct_name(model_weight)}_model_{_pct_name(1 - model_weight)}_market",
                f"{round(model_weight * 100)}% model probability + {round((1 - model_weight) * 100)}% market probability",
                "blend",
                lambda model, market, weight=model_weight: blend_probability(model, market, weight),
            )
            for model_weight in [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
        ],
        *[
            _variant(
                f"model_shrink_{int(shrink * 100):02d}",
                f"Current model probability shrunk {int(shrink * 100)}% toward 50/50",
                "calibration",
                lambda model, market, amount=shrink: shrink_to_even(model, amount),
            )
            for shrink in [0.25, 0.5, 0.75]
        ],
        *[
            _variant(
                f"blend_25_model_75_market_shrink_{int(shrink * 100):02d}",
                f"25/75 model-market blend shrunk {int(shrink * 100)}% toward 50/50",
                "calibrated_blend",
                lambda model, market, amount=shrink: shrink_to_even(
                    blend_probability(model, market, 0.25), amount
                ),
            )
            for shrink in [0.25, 0.5]
        ],
    ]
    reports = [_evaluate_variant(variant, samples, markets) for variant in variants]
    market = next(report for report in reports if report["name"] == "market_favorite")
    market_roi = market["simulated_research_roi"]["roi_pct"]
    for report in reports:
        report["roi_delta_vs_market_favorite"] = roi_delta(
            report["simulated_research_roi"]["roi_pct"], market_roi
        )
        report["clears_market_roi_gate"] = (
            report["roi_delta_vs_market_favorite"] is not None
            and report["roi_delta_vs_market_favorite"] >= MIN_MARKET_ROI_DELTA
        )
    best_candidate = max(
        (report for report in reports if report["name"] != "market_favorite"),
        key=lambda report: report["simulated_research_roi"]["roi_pct"] or float("-inf"),
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "market-aware-blend-experiments",
        "report_only": True,
        "writes_model_versions": False,
        "value_status": "research_only",
        "value_status_reason": (
            "Calibration and blend variants are report-only until a candidate beats the no-vig "
            "market favorite by the configured ROI gate."
        ),
        "input_manifest": "data/experiments/market-aware-model-experiment-manifest.json",
        "coverage": {
            **coverage["summary"],
            "scored_events": len({sample["event_id"] for sample in samples}),
            "scored_fights": len(samples),
        },
        "market_baseline": {
            "name": "market_favorite",
            "roi_pct": market_roi,
            "accuracy": market["metrics"]["accuracy"],
            "log_loss": market["metrics"]["log_loss"],
            "brier_score": market["metrics"]["brier_score"],
        },
        "gate": {
            "min_roi_delta_vs_market_favorite": MIN_MARKET_ROI_DELTA,
            "best_candidate": best_candidate["name"],
            "best_candidate_roi_pct": best_candidate["simulated_research_roi"]["roi_pct"],
            "best_candidate_roi_delta_vs_market_favorite": best_candidate[
                "roi_delta_vs_market_favorite"
            ],
            "candidate_cleared_gate": best_candidate["clears_market_roi_gate"],
        },
        "variants": reports,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Market-Aware Blend Experiments",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Value status: `{report['value_status']}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Scored events: {report['coverage']['scored_events']}",
        f"- Scored fights: {report['coverage']['scored_fights']}",
        "",
        "## Gate",
        "",
        f"- Market favorite ROI: {_fmt_pct(report['market_baseline']['roi_pct'])}",
        f"- Best candidate: `{report['gate']['best_candidate']}`",
        f"- Best candidate ROI: {_fmt_pct(report['gate']['best_candidate_roi_pct'])}",
        f"- Delta vs market favorite: {_fmt_signed_pct(report['gate']['best_candidate_roi_delta_vs_market_favorite'])}",
        f"- Candidate cleared +2pp gate: `{str(report['gate']['candidate_cleared_gate']).lower()}`",
        "",
        "## Variants",
        "",
        "| Variant | Family | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for variant in report["variants"]:
        metrics = variant["metrics"]
        roi = variant["simulated_research_roi"]
        lines.append(
            "| {name} | {family} | {accuracy} | {log_loss} | {brier} | {roi} | {delta} | {clears} |".format(
                name=variant["name"],
                family=variant["family"],
                accuracy=_fmt_pct(metrics["accuracy"]),
                log_loss=_fmt_metric(metrics["log_loss"]),
                brier=_fmt_metric(metrics["brier_score"]),
                roi=_fmt_pct(roi["roi_pct"]),
                delta=_fmt_signed_pct(variant["roi_delta_vs_market_favorite"]),
                clears=str(variant["clears_market_roi_gate"]).lower(),
            )
        )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            report["value_status_reason"],
            "This experiment does not save model files, write `model_versions`, or activate value claims.",
        ]
    )
    return "\n".join(lines)


def blend_probability(model_probability: float, market_probability: float, model_weight: float) -> float:
    return _clip_probability(model_weight * model_probability + (1 - model_weight) * market_probability)


def shrink_to_even(probability: float, amount: float) -> float:
    return _clip_probability(0.5 + (1 - amount) * (probability - 0.5))


def roi_delta(candidate_roi: float | None, market_roi: float | None) -> float | None:
    if candidate_roi is None or market_roi is None:
        return None
    return candidate_roi - market_roi


def _variant(name: str, description: str, family: str, probability_fn: ProbabilityFn) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "family": family,
        "probability_fn": probability_fn,
    }


def _evaluate_variant(
    variant: dict[str, Any],
    samples: list[dict[str, Any]],
    markets: dict[str, dict[str, dict[str, float]]],
) -> dict[str, Any]:
    predictions = [_prediction_for_sample(sample, markets, variant["probability_fn"]) for sample in samples]
    return {
        "name": variant["name"],
        "description": variant["description"],
        "family": variant["family"],
        "metrics": _metrics(predictions),
        "simulated_research_roi": _roi(predictions),
    }


def _prediction_for_sample(
    sample: dict[str, Any],
    markets: dict[str, dict[str, dict[str, float]]],
    probability_fn: ProbabilityFn,
) -> dict[str, Any]:
    market = markets[sample["fight_id"]]
    model_probability = _ufc_experience_probability(sample)
    market_probability = market[sample["fighter_a_id"]]["market_prob"]
    fighter_a_probability = probability_fn(model_probability, market_probability)
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


def _clip_probability(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError("probability must be finite")
    return min(0.999, max(0.001, value))


def _fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _fmt_signed_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:+.1f}pp"


def _fmt_metric(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def _pct_name(value: float) -> str:
    return f"{round(value * 100):02d}"


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run report-only market-aware blend experiments")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_market_blend_experiments(output_path=output_path, markdown_path=markdown_path)
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
        "gate": report["gate"],
        "market_baseline": report["market_baseline"],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
