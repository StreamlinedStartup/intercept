"""Refresh report-only market indicator snapshots for upcoming fights."""
from __future__ import annotations

import argparse
import json
import subprocess
from collections.abc import Callable, Iterable
from datetime import UTC, date, datetime
from typing import Any

from psycopg.rows import dict_row

from ml import prop_indicators

TARGET = prop_indicators.OVER_2_5_TARGET
INDICATOR_NAME = "locked_over_2_5_positive_edge"
SOURCE_REPORT = "refresh-upcoming-indicators"

type FightRow = dict[str, Any]
type Market = dict[str, float | int]
type Snapshot = dict[str, Any]


def refresh_upcoming_indicators(
    *,
    today: date | None = None,
    computed_at: datetime | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Load upcoming fights from Postgres and materialize report-only indicator snapshots."""
    from ml.db import pool

    today = today or date.today()
    computed_at = computed_at or datetime.now(UTC)
    with pool.borrow() as conn:
        rows = _load_upcoming_rows(conn, today)
        summary = refresh_indicator_rows(
            rows,
            computed_at=computed_at,
            indicator_fn=_over_2_5_indicator,
            market_fn=lambda fight_id: _load_over_2_5_market(conn, fight_id),
            write_fn=lambda snapshot: _upsert_indicator_snapshot(conn, snapshot),
            dry_run=dry_run,
        )
        if not dry_run:
            conn.commit()
    return summary


def refresh_indicator_rows(
    rows: Iterable[FightRow],
    *,
    computed_at: datetime,
    indicator_fn: Callable[[FightRow, FightRow], dict[str, Any]],
    market_fn: Callable[[str], Market | None],
    write_fn: Callable[[Snapshot], None],
    dry_run: bool = False,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "scanned": 0,
        "written": 0,
        "skipped": 0,
        "missing_props": 0,
        "errors": 0,
        "skip_reasons": [],
        "error_details": [],
        "dry_run": dry_run,
    }
    for fight_id, fight_rows in _group_by_fight(rows).items():
        summary["scanned"] += 1
        if len(fight_rows) != 2:
            _skip(summary, fight_id, "fight must have exactly two participants")
            continue
        not_current = [row for row in fight_rows if row.get("backfill_status") != "current"]
        if not_current:
            _skip(
                summary,
                fight_id,
                "both fighters must have current backfill state",
                {
                    "fighters": [
                        {
                            "fighter_id": row["fighter_id"],
                            "backfill_status": row.get("backfill_status") or "none",
                        }
                        for row in fight_rows
                    ]
                },
            )
            continue

        fighter_a, fighter_b = fight_rows
        try:
            model = indicator_fn(fighter_a, fighter_b)
            market = market_fn(fight_id)
            if market is None:
                summary["missing_props"] += 1
            snapshot = _snapshot_from_indicator(
                fight_id=fight_id,
                model=model,
                market=market,
                computed_at=computed_at,
            )
            if not dry_run:
                write_fn(snapshot)
            summary["written"] += 1
        except Exception as exc:  # noqa: BLE001 - batch job reports per-fight failures and continues.
            summary["errors"] += 1
            summary["error_details"].append({"fight_id": fight_id, "reason": str(exc)})
    return summary


def _load_upcoming_rows(conn: Any, today: date) -> list[FightRow]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT
                f.id AS fight_id,
                e.id AS event_id,
                e.date AS event_date,
                f.weight_class,
                fr.fighter_id,
                fbs.status AS backfill_status
            FROM events e
            JOIN fights f ON f.event_id = e.id
            JOIN fight_results fr ON fr.fight_id = f.id
            LEFT JOIN fighter_backfill_state fbs ON fbs.fighter_id = fr.fighter_id
            WHERE e.completed = false
                AND e.date >= %s
            ORDER BY e.date ASC, f.is_headliner DESC, f.id ASC, fr.fighter_id ASC
            """,
            (today,),
        )
        return list(cur.fetchall())


def _over_2_5_indicator(fighter_a: FightRow, fighter_b: FightRow) -> dict[str, Any]:
    return prop_indicators.over_2_5_indicator(
        str(fighter_a["fighter_id"]),
        str(fighter_b["fighter_id"]),
        _date_string(fighter_a["event_date"]),
        fighter_a.get("weight_class"),
    )


def _load_over_2_5_market(conn: Any, fight_id: str) -> Market | None:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT
                hpo.source_market_id,
                hpo.sportsbook_slug,
                hpo.outcome_side,
                hpo.implied_probability
            FROM historical_prop_odds hpo
            JOIN historical_odds_fights hof ON hof.id = hpo.historical_fight_id
            WHERE hof.canonical_fight_id = %s
                AND hpo.source_offer_type_id = 'OVERUNDER_2.5'
                AND hpo.line_kind = 'source_current'
            """,
            (fight_id,),
        )
        return over_2_5_no_vig_market(cur.fetchall())


def over_2_5_no_vig_market(rows: Iterable[dict[str, Any]]) -> Market | None:
    pairs: dict[str, dict[str, float]] = {}
    for row in rows:
        key = f"{row['source_market_id']}:{row['sportsbook_slug']}"
        pair = pairs.setdefault(key, {})
        if row["outcome_side"] == "outcome1":
            pair["outcome1"] = float(row["implied_probability"])
        if row["outcome_side"] == "outcome2":
            pair["outcome2"] = float(row["implied_probability"])
    probabilities = []
    for pair in pairs.values():
        over = pair.get("outcome1")
        under = pair.get("outcome2")
        if over is None or under is None:
            continue
        total = over + under
        if total > 0:
            probabilities.append(over / total)
    if not probabilities:
        return None
    return {
        "market_probability": sum(probabilities) / len(probabilities),
        "pair_count": len(probabilities),
    }


def _snapshot_from_indicator(
    *,
    fight_id: str,
    model: dict[str, Any],
    market: Market | None,
    computed_at: datetime,
) -> Snapshot:
    model_probability = model.get("model_probability")
    market_probability = None if market is None else float(market["market_probability"])
    edge_pct = (
        None
        if model_probability is None or market_probability is None
        else float(model_probability) - market_probability
    )
    return {
        "fight_id": fight_id,
        "target": TARGET,
        "model_version": str(model["model_version"]),
        "indicator_name": INDICATOR_NAME,
        "computed_at": computed_at,
        "model_probability": model_probability,
        "market_probability": market_probability,
        "edge_pct": edge_pct,
        "candidate": bool(model.get("candidate")),
        "market_pair_count": 0 if market is None else int(market["pair_count"]),
        "value_status": _value_status(model, market),
        "source_report": SOURCE_REPORT,
        "source_config": json.dumps(
            {
                "target": TARGET,
                "threshold": model.get("threshold"),
                "indicator_name": INDICATOR_NAME,
            },
            sort_keys=True,
        ),
        "source_git_sha": _git_sha(),
        "source_model_path": str(prop_indicators.OVER_2_5_ARTIFACT_PATH),
        "source_data_window": "events.completed=false and events.date>=today",
        "staleness_reason": None if market is not None else "missing_over_2_5_market",
        "raw_metadata": json.dumps(
            {
                "label": model.get("label"),
                "value_status_reason": model.get("value_status_reason"),
                "training_sample_count": model.get("training_sample_count"),
                "artifact_generated_at": model.get("artifact_generated_at"),
                "dry_run_safe": True,
            },
            sort_keys=True,
        ),
    }


def _upsert_indicator_snapshot(conn: Any, snapshot: Snapshot) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO market_indicator_snapshots (
                fight_id,
                target,
                model_version,
                indicator_name,
                computed_at,
                model_probability,
                market_probability,
                edge_pct,
                candidate,
                market_pair_count,
                value_status,
                source_report,
                source_config,
                source_git_sha,
                source_model_path,
                source_data_window,
                staleness_reason,
                raw_metadata
            )
            VALUES (
                %(fight_id)s,
                %(target)s,
                %(model_version)s,
                %(indicator_name)s,
                %(computed_at)s,
                %(model_probability)s,
                %(market_probability)s,
                %(edge_pct)s,
                %(candidate)s,
                %(market_pair_count)s,
                %(value_status)s,
                %(source_report)s,
                %(source_config)s,
                %(source_git_sha)s,
                %(source_model_path)s,
                %(source_data_window)s,
                %(staleness_reason)s,
                %(raw_metadata)s
            )
            ON CONFLICT (fight_id, target, model_version, indicator_name)
            DO UPDATE SET
                computed_at = EXCLUDED.computed_at,
                model_probability = EXCLUDED.model_probability,
                market_probability = EXCLUDED.market_probability,
                edge_pct = EXCLUDED.edge_pct,
                candidate = EXCLUDED.candidate,
                market_pair_count = EXCLUDED.market_pair_count,
                value_status = EXCLUDED.value_status,
                source_report = EXCLUDED.source_report,
                source_config = EXCLUDED.source_config,
                source_git_sha = EXCLUDED.source_git_sha,
                source_model_path = EXCLUDED.source_model_path,
                source_data_window = EXCLUDED.source_data_window,
                staleness_reason = EXCLUDED.staleness_reason,
                raw_metadata = EXCLUDED.raw_metadata,
                updated_at = now()
            """,
            snapshot,
        )


def _group_by_fight(rows: Iterable[FightRow]) -> dict[str, list[FightRow]]:
    grouped: dict[str, list[FightRow]] = {}
    for row in rows:
        grouped.setdefault(str(row["fight_id"]), []).append(row)
    return grouped


def _skip(
    summary: dict[str, Any],
    fight_id: str,
    reason: str,
    extra: dict[str, Any] | None = None,
) -> None:
    summary["skipped"] += 1
    detail = {"fight_id": fight_id, "reason": reason}
    if extra:
        detail.update(extra)
    summary["skip_reasons"].append(detail)


def _value_status(model: dict[str, Any], market: Market | None) -> str:
    if model.get("value_status") == "insufficient_training" or model.get("model_probability") is None:
        return "insufficient_training"
    if market is None:
        return "insufficient_coverage"
    return "report_only"


def _date_string(value: Any) -> str:
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:  # noqa: BLE001 - source metadata is useful but optional.
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Compute snapshots without writing them.")
    parser.add_argument("--today", help="Override the lower-bound date for upcoming fights, YYYY-MM-DD.")
    args = parser.parse_args()
    today = date.fromisoformat(args.today) if args.today else None
    summary = refresh_upcoming_indicators(today=today, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
