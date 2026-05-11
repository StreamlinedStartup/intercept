"""One-event odds-aware evaluation report for matched FightOdds data."""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any

from psycopg.rows import dict_row

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EVENT_ID = "902ab9197b83d0db"
DEFAULT_SOURCE_EVENT_ID = "5362"
DEFAULT_JSON_OUTPUT = REPO_ROOT / "data" / "experiments" / "odds-aware-one-event.json"
DEFAULT_MARKDOWN_OUTPUT = REPO_ROOT / "data" / "experiments" / "odds-aware-one-event.md"


def american_to_implied_probability(american_odds: int) -> float:
    if american_odds == 0:
        raise ValueError("American odds cannot be zero")
    if american_odds > 0:
        return 100 / (american_odds + 100)
    return -american_odds / (-american_odds + 100)


def decimal_from_american(american_odds: int) -> float:
    if american_odds == 0:
        raise ValueError("American odds cannot be zero")
    if american_odds > 0:
        return 1 + american_odds / 100
    return 1 + 100 / -american_odds


def remove_vig(probability_a: float, probability_b: float) -> tuple[float, float]:
    total = probability_a + probability_b
    if total <= 0:
        raise ValueError("Cannot remove vig from non-positive probabilities")
    return probability_a / total, probability_b / total


def edge(model_probability: float, market_probability: float) -> float:
    return model_probability - market_probability


def flat_stake_net_profit(decimal_odds: float, won: bool) -> float:
    if decimal_odds <= 1:
        raise ValueError("Decimal odds must be greater than 1")
    return decimal_odds - 1 if won else -1.0


def run_odds_aware_report(
    *,
    event_id: str = DEFAULT_EVENT_ID,
    source_event_id: str = DEFAULT_SOURCE_EVENT_ID,
    output_path: Path = DEFAULT_JSON_OUTPUT,
    markdown_path: Path = DEFAULT_MARKDOWN_OUTPUT,
    min_train_samples: int = 200,
) -> dict[str, Any]:
    event_predictions = _build_event_predictions(event_id, min_train_samples)
    market = _load_consensus_market(source_event_id)
    report = _build_report(event_predictions, market, source_event_id, min_train_samples)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report) + "\n")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    rows = report["fights"]
    lines = [
        f"# Odds-Aware Report: {report['event']['name']}",
        "",
        f"- Event date: {report['event']['date']}",
        f"- Source event: FightOdds {report['source_event_id']}",
        f"- Matched fights scored: {report['summary']['fights_scored']}",
        f"- Model-edge bets: {report['roi']['model_edge']['bets']}, ROI {_format_pct(report['roi']['model_edge']['roi'])}",
        f"- Market-favorite baseline: {report['roi']['market_favorite']['bets']} bets, ROI {_format_pct(report['roi']['market_favorite']['roi'])}",
        "",
        "## Timestamp Semantics",
        "",
        report["timestamp_semantics"]["label"],
        "",
        "## Fight Rows",
        "",
        "| Fight | Model pick | Model prob | Market no-vig | Edge | Result | Avg decimal |",
        "|---|---|---:|---:|---:|---|---:|",
    ]
    for row in rows:
        lines.append(
            "| {fight} | {pick} | {model_prob} | {market_prob} | {edge} | {result} | {decimal_odds} |".format(
                fight=f"{row['fighter_a']['name']} vs {row['fighter_b']['name']}",
                pick=row["model_pick"]["name"],
                model_prob=_format_pct(row["model_pick"]["model_probability"]),
                market_prob=_format_pct(row["model_pick"]["market_no_vig_probability"]),
                edge=_format_signed_pct(row["model_pick"]["edge"]),
                result="win" if row["model_pick"]["won"] else "loss",
                decimal_odds=f"{row['model_pick']['average_decimal_odds']:.3f}",
            )
        )
    lines.extend(
        [
            "",
            "## Buckets",
            "",
            "### Confidence",
            "",
            "| Bucket | Count | Accuracy | ROI |",
            "|---|---:|---:|---:|",
        ]
    )
    for bucket in report["by_confidence_bucket"]:
        lines.append(_bucket_row(bucket))
    lines.extend(["", "### Edge", "", "| Bucket | Count | Accuracy | ROI |", "|---|---:|---:|---:|"])
    for bucket in report["by_edge_bucket"]:
        lines.append(_bucket_row(bucket))
    lines.extend(
        [
            "",
            "## Secondary Model Metrics",
            "",
            "| Accuracy | Log loss | Brier | ROC AUC |",
            "|---:|---:|---:|---:|",
            "| {accuracy} | {log_loss} | {brier} | {roc_auc} |".format(
                accuracy=_format_metric(report["secondary_model_metrics"]["accuracy"]),
                log_loss=_format_metric(report["secondary_model_metrics"]["log_loss"]),
                brier=_format_metric(report["secondary_model_metrics"]["brier_score"]),
                roc_auc=_format_metric(report["secondary_model_metrics"]["roc_auc"]),
            ),
        ]
    )
    return "\n".join(lines)


def _build_event_predictions(event_id: str, min_train_samples: int) -> dict[str, Any]:
    from ml.backtest import _build_samples, _fit_model, _load_completed_fights, _metrics, _predict_sample

    rows = _load_completed_fights()
    event_row = next((row for row in rows if row["event_id"] == event_id), None)
    if event_row is None:
        raise ValueError(f"Event {event_id!r} is not available in completed UFC fights")

    samples = _build_samples(
        [row for row in rows if row["event_date"] <= event_row["event_date"]],
        feature_names=None,
    )
    train_samples = [sample for sample in samples if sample["event_date"] < event_row["event_date"]]
    target_samples = [sample for sample in samples if sample["event_id"] == event_id]
    if len(train_samples) < min_train_samples:
        raise ValueError(
            f"Event {event_id!r} has only {len(train_samples)} train samples; need {min_train_samples}"
        )
    model = _fit_model(train_samples)
    predictions = [_predict_sample(model, sample) for sample in target_samples]
    fighters = _load_fight_fighters(event_id)
    return {
        "event": {
            "id": event_id,
            "name": event_row["event_name"],
            "date": event_row["event_date"].isoformat(),
            "train_samples": len(train_samples),
        },
        "predictions": predictions,
        "fighters": fighters,
        "metrics": _metrics(predictions),
    }


def _load_fight_fighters(event_id: str) -> dict[str, dict[str, Any]]:
    from ml.db import pool

    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    f.id AS fight_id,
                    fr.fighter_id,
                    fi.name AS fighter_name,
                    fr.outcome
                FROM fights f
                JOIN fight_results fr ON fr.fight_id = f.id
                JOIN fighters fi ON fi.id = fr.fighter_id
                WHERE f.event_id = %s
                    AND fr.outcome IN ('win', 'loss')
                ORDER BY f.id, fr.fighter_id
                """,
                (event_id,),
            )
            rows = cur.fetchall()

    by_fight: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_fight[str(row["fight_id"])].append(row)

    return {
        fight_id: {
            "fighter_a": {
                "id": rows_for_fight[0]["fighter_id"],
                "name": rows_for_fight[0]["fighter_name"],
                "outcome": rows_for_fight[0]["outcome"],
            },
            "fighter_b": {
                "id": rows_for_fight[1]["fighter_id"],
                "name": rows_for_fight[1]["fighter_name"],
                "outcome": rows_for_fight[1]["outcome"],
            },
        }
        for fight_id, rows_for_fight in by_fight.items()
        if len(rows_for_fight) == 2
    }


def _load_consensus_market(source_event_id: str) -> dict[str, Any]:
    from ml.db import pool

    with pool.borrow() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    hof.canonical_fight_id,
                    hmo.source_offer_id,
                    hmo.sportsbook_name,
                    hmo.canonical_fighter_id,
                    hmo.american_odds,
                    hmo.decimal_odds,
                    hmo.market_timestamp_semantics
                FROM historical_moneyline_odds hmo
                JOIN historical_odds_fights hof ON hof.id = hmo.historical_fight_id
                JOIN historical_odds_events hoe ON hoe.id = hof.historical_event_id
                WHERE hoe.source = 'fightodds'
                    AND hoe.source_event_id = %s
                    AND hof.match_status = 'matched'
                    AND hof.canonical_fight_id IS NOT NULL
                    AND hmo.canonical_fighter_id IS NOT NULL
                    AND hmo.line_kind = 'source_current'
                ORDER BY hof.canonical_fight_id, hmo.source_offer_id, hmo.canonical_fighter_id
                """,
                (source_event_id,),
            )
            rows = cur.fetchall()

    by_offer: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    semantics = set()
    for row in rows:
        by_offer[(str(row["canonical_fight_id"]), str(row["source_offer_id"]))].append(row)
        semantics.add(str(row["market_timestamp_semantics"]))

    fighter_markets: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    fight_offer_count: dict[str, int] = defaultdict(int)
    for (fight_id, _offer_id), offer_rows in by_offer.items():
        distinct = {row["canonical_fighter_id"]: row for row in offer_rows}
        if len(distinct) != 2:
            continue
        [left, right] = distinct.values()
        left_implied = american_to_implied_probability(int(left["american_odds"]))
        right_implied = american_to_implied_probability(int(right["american_odds"]))
        left_no_vig, right_no_vig = remove_vig(left_implied, right_implied)
        for row, no_vig in [(left, left_no_vig), (right, right_no_vig)]:
            fighter_id = str(row["canonical_fighter_id"])
            fighter_markets[fight_id][fighter_id].append(no_vig)
            fighter_markets[fight_id][f"{fighter_id}:decimal"].append(float(row["decimal_odds"]))
        fight_offer_count[fight_id] += 1

    consensus: dict[str, dict[str, dict[str, float]]] = {}
    for fight_id, values_by_fighter in fighter_markets.items():
        consensus[fight_id] = {}
        for fighter_id, values in values_by_fighter.items():
            if fighter_id.endswith(":decimal"):
                continue
            decimal_values = values_by_fighter[f"{fighter_id}:decimal"]
            consensus[fight_id][fighter_id] = {
                "no_vig_probability": mean(values),
                "average_decimal_odds": mean(decimal_values),
                "offer_count": float(len(values)),
            }

    return {
        "consensus": consensus,
        "offer_counts": dict(fight_offer_count),
        "semantics": sorted(semantics),
        "raw_rows": len(rows),
        "complete_offer_pairs": sum(fight_offer_count.values()),
    }


def _build_report(
    event_predictions: dict[str, Any],
    market: dict[str, Any],
    source_event_id: str,
    min_train_samples: int,
) -> dict[str, Any]:
    fights = []
    for prediction in event_predictions["predictions"]:
        fight_id = prediction["fight_id"]
        fighters = event_predictions["fighters"].get(fight_id)
        fight_market = market["consensus"].get(fight_id)
        if fighters is None or fight_market is None:
            continue
        row = _fight_report_row(prediction, fighters, fight_market, market["offer_counts"].get(fight_id, 0))
        fights.append(row)

    model_edge_bets = [row["model_pick"] for row in fights if row["model_pick"]["edge"] > 0]
    market_favorite_bets = [row["market_favorite"] for row in fights]
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "report": "one-event-odds-aware",
        "source_event_id": source_event_id,
        "event": event_predictions["event"],
        "args": {"min_train_samples": min_train_samples},
        "summary": {
            "fights_scored": len(fights),
            "walk_forward_predictions": len(event_predictions["predictions"]),
            "historical_moneyline_rows": market["raw_rows"],
            "complete_offer_pairs": market["complete_offer_pairs"],
        },
        "timestamp_semantics": {
            "observed_values": market["semantics"],
            "label": (
                "FightOdds source_current lines are captured at import scrape time. "
                "They are usable as close/current market consensus for this slice, "
                "not as true point-in-time historical snapshots."
            ),
        },
        "roi": {
            "model_edge": _roi_summary(model_edge_bets),
            "market_favorite": _roi_summary(market_favorite_bets),
        },
        "calibration_vs_market": _market_calibration(fights),
        "by_confidence_bucket": _bucket_summaries(fights, "confidence_bucket"),
        "by_edge_bucket": _bucket_summaries(fights, "edge_bucket"),
        "secondary_model_metrics": {
            "accuracy": event_predictions["metrics"]["accuracy"],
            "log_loss": event_predictions["metrics"]["log_loss"],
            "brier_score": event_predictions["metrics"]["brier_score"],
            "roc_auc": event_predictions["metrics"]["roc_auc"],
        },
        "fights": fights,
    }


def _fight_report_row(
    prediction: dict[str, Any],
    fighters: dict[str, Any],
    fight_market: dict[str, dict[str, float]],
    offer_count: int,
) -> dict[str, Any]:
    fighter_a = fighters["fighter_a"]
    fighter_b = fighters["fighter_b"]
    fighter_a_probability = float(prediction["fighter_a_win_prob"])
    fighter_rows = [
        _fighter_side_row(fighter_a, fighter_a_probability, fight_market),
        _fighter_side_row(fighter_b, 1 - fighter_a_probability, fight_market),
    ]
    model_pick = max(fighter_rows, key=lambda row: row["model_probability"])
    market_favorite = max(fighter_rows, key=lambda row: row["market_no_vig_probability"])
    for row in fighter_rows:
        row["edge"] = edge(row["model_probability"], row["market_no_vig_probability"])
        row["won"] = row["outcome"] == "win"
        row["net_profit"] = flat_stake_net_profit(row["average_decimal_odds"], row["won"])
    return {
        "fight_id": prediction["fight_id"],
        "fighter_a": fighter_rows[0],
        "fighter_b": fighter_rows[1],
        "model_pick": model_pick,
        "market_favorite": market_favorite,
        "confidence_bucket": _confidence_bucket(model_pick["model_probability"]),
        "edge_bucket": _edge_bucket(model_pick["edge"]),
        "complete_offer_pairs": offer_count,
    }


def _fighter_side_row(
    fighter: dict[str, Any],
    model_probability: float,
    fight_market: dict[str, dict[str, float]],
) -> dict[str, Any]:
    market = fight_market[fighter["id"]]
    return {
        "id": fighter["id"],
        "name": fighter["name"],
        "outcome": fighter["outcome"],
        "model_probability": model_probability,
        "market_no_vig_probability": market["no_vig_probability"],
        "average_decimal_odds": market["average_decimal_odds"],
        "offer_count": int(market["offer_count"]),
    }


def _roi_summary(bets: list[dict[str, Any]]) -> dict[str, Any]:
    staked = len(bets)
    net_profit = sum(float(bet["net_profit"]) for bet in bets)
    return {
        "bets": staked,
        "wins": sum(1 for bet in bets if bet["won"]),
        "staked": staked,
        "net_profit": net_profit,
        "roi": None if staked == 0 else net_profit / staked,
    }


def _market_calibration(fights: list[dict[str, Any]]) -> dict[str, Any]:
    favorites = [row["market_favorite"] for row in fights]
    if not favorites:
        return {
            "market_favorite_accuracy": None,
            "average_market_favorite_probability": None,
            "calibration_gap": None,
        }
    accuracy = sum(1 for favorite in favorites if favorite["won"]) / len(favorites)
    avg_probability = mean(favorite["market_no_vig_probability"] for favorite in favorites)
    return {
        "market_favorite_accuracy": accuracy,
        "average_market_favorite_probability": avg_probability,
        "calibration_gap": accuracy - avg_probability,
    }


def _bucket_summaries(fights: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in fights:
        grouped[row[key]].append(row["model_pick"])
    return [
        {
            "bucket": bucket,
            **_accuracy_summary(rows),
            **_roi_summary(rows),
        }
        for bucket, rows in sorted(grouped.items(), key=lambda item: _bucket_sort_key(item[0]))
    ]


def _accuracy_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"count": 0, "accuracy": None}
    return {
        "count": len(rows),
        "accuracy": sum(1 for row in rows if row["won"]) / len(rows),
    }


def _confidence_bucket(probability: float) -> str:
    confidence = max(probability, 1 - probability)
    if confidence < 0.55:
        return "50-55"
    if confidence < 0.60:
        return "55-60"
    if confidence < 0.65:
        return "60-65"
    if confidence < 0.70:
        return "65-70"
    return "70+"


def _edge_bucket(value: float) -> str:
    if value < 0:
        return "negative"
    if value < 0.02:
        return "0-2"
    if value < 0.05:
        return "2-5"
    if value < 0.10:
        return "5-10"
    return "10+"


def _bucket_sort_key(bucket: str) -> tuple[int, str]:
    order = {"negative": -1, "50-55": 50, "55-60": 55, "60-65": 60, "65-70": 65, "70+": 70}
    return (order.get(bucket, 999), bucket)


def _bucket_row(bucket: dict[str, Any]) -> str:
    return "| {bucket} | {count} | {accuracy} | {roi} |".format(
        bucket=bucket["bucket"],
        count=bucket["count"],
        accuracy=_format_pct(bucket["accuracy"]),
        roi=_format_pct(bucket["roi"]),
    )


def _format_metric(value: Any) -> str:
    return "" if value is None else f"{float(value):.4f}"


def _format_pct(value: Any) -> str:
    return "" if value is None else f"{float(value) * 100:.1f}%"


def _format_signed_pct(value: Any) -> str:
    return "" if value is None else f"{float(value) * 100:+.1f}%"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce one-event odds-aware model report")
    parser.add_argument("--event-id", default=DEFAULT_EVENT_ID)
    parser.add_argument("--source-event-id", default=DEFAULT_SOURCE_EVENT_ID)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--min-train-samples", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    markdown_path = args.markdown if args.markdown.is_absolute() else REPO_ROOT / args.markdown
    report = run_odds_aware_report(
        event_id=args.event_id,
        source_event_id=args.source_event_id,
        output_path=output_path,
        markdown_path=markdown_path,
        min_train_samples=args.min_train_samples,
    )
    print(
        json.dumps(
            {
                "output_path": str(output_path.relative_to(REPO_ROOT)),
                "markdown_path": str(markdown_path.relative_to(REPO_ROOT)),
                "fights_scored": report["summary"]["fights_scored"],
                "model_edge_roi": report["roi"]["model_edge"]["roi"],
                "market_favorite_roi": report["roi"]["market_favorite"]["roi"],
            },
            indent=2,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
