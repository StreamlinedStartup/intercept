"""Point-in-time feature construction for UFC fight prediction."""
from __future__ import annotations

import math
from datetime import date
from typing import Any

import numpy as np

from ml.db import pool

FEATURE_NAMES = [
    "slpm_diff",
    "str_acc_diff",
    "sapm_diff",
    "str_def_diff",
    "td_avg_diff",
    "td_acc_diff",
    "td_def_diff",
    "sub_avg_diff",
    "height_diff",
    "reach_diff",
    "age_diff",
]


def build_features(fight_id: str) -> tuple[np.ndarray, float]:
    """Build the minimal Phase 3 feature row for one fight.

    Aggregates only fights whose event date is strictly before the target fight
    date. The returned label is 1.0 when fighter A won, 0.0 when fighter B won,
    and NaN when the target fight does not have a win/loss result yet.
    """
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    f.id AS fight_id,
                    e.date AS event_date,
                    fr.fighter_id,
                    fr.opponent_id,
                    fr.outcome,
                    fi.dob,
                    fi.height_in,
                    fi.reach_in
                FROM fights f
                JOIN events e ON e.id = f.event_id
                JOIN fight_results fr ON fr.fight_id = f.id
                JOIN fighters fi ON fi.id = fr.fighter_id
                WHERE f.id = %s
                ORDER BY fr.fighter_id
                """,
                (fight_id,),
            )
            rows = cur.fetchall()
            if len(rows) != 2:
                raise ValueError(f"fight_id {fight_id!r} must have exactly two fighter rows")

            fighter_a = _row_dict(cur.description, rows[0])
            fighter_b = _row_dict(cur.description, rows[1])
            target_date = fighter_a["event_date"]

    return (
        build_feature_row(fighter_a["fighter_id"], fighter_b["fighter_id"], target_date),
        _label(fighter_a["outcome"], fighter_b["outcome"]),
    )


def build_feature_row(fighter_a_id: str, fighter_b_id: str, fight_date: date) -> np.ndarray:
    """Build features for a caller-specified fighter order."""
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            fighter_a = _load_fighter(cur, fighter_a_id)
            fighter_b = _load_fighter(cur, fighter_b_id)
            stats_a = _career_stats(cur, fighter_a_id, fight_date)
            stats_b = _career_stats(cur, fighter_b_id, fight_date)

    return np.array(
        [
            _diff(stats_a["slpm"], stats_b["slpm"]),
            _diff(stats_a["str_acc"], stats_b["str_acc"]),
            _diff(stats_a["sapm"], stats_b["sapm"]),
            _diff(stats_a["str_def"], stats_b["str_def"]),
            _diff(stats_a["td_avg"], stats_b["td_avg"]),
            _diff(stats_a["td_acc"], stats_b["td_acc"]),
            _diff(stats_a["td_def"], stats_b["td_def"]),
            _diff(stats_a["sub_avg"], stats_b["sub_avg"]),
            _diff(_maybe_float(fighter_a["height_in"]), _maybe_float(fighter_b["height_in"])),
            _diff(_maybe_float(fighter_a["reach_in"]), _maybe_float(fighter_b["reach_in"])),
            _diff(_age_years(fighter_a["dob"], fight_date), _age_years(fighter_b["dob"], fight_date)),
        ],
        dtype=float,
    )


def _load_fighter(cur: Any, fighter_id: str) -> dict[str, Any]:
    cur.execute(
        """
        SELECT id, dob, height_in, reach_in
        FROM fighters
        WHERE id = %s
        """,
        (fighter_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"fighter_id {fighter_id!r} was not found")
    return _row_dict(cur.description, row)


def _career_stats(cur: Any, fighter_id: str, target_date: date) -> dict[str, float]:
    cur.execute(
        """
        SELECT
            fr.sig_strikes_landed,
            fr.sig_strikes_attempted,
            fr.total_strikes_landed,
            fr.total_strikes_attempted,
            fr.takedowns_landed,
            fr.takedowns_attempted,
            fr.sub_attempts,
            fr.time_seconds,
            opp.sig_strikes_landed AS opp_sig_strikes_landed,
            opp.sig_strikes_attempted AS opp_sig_strikes_attempted,
            opp.takedowns_landed AS opp_takedowns_landed,
            opp.takedowns_attempted AS opp_takedowns_attempted
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        LEFT JOIN fight_results opp
            ON opp.fight_id = fr.fight_id
            AND opp.fighter_id = fr.opponent_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    total_seconds = _sum(rows, "time_seconds")
    minutes = total_seconds / 60 if total_seconds > 0 else math.nan
    return {
        "slpm": _per_minute(_sum(rows, "sig_strikes_landed"), minutes),
        "str_acc": _ratio(_sum(rows, "sig_strikes_landed"), _sum(rows, "sig_strikes_attempted")),
        "sapm": _per_minute(_sum(rows, "opp_sig_strikes_landed"), minutes),
        "str_def": _defense(_sum(rows, "opp_sig_strikes_landed"), _sum(rows, "opp_sig_strikes_attempted")),
        "td_avg": _per_15(_sum(rows, "takedowns_landed"), minutes),
        "td_acc": _ratio(_sum(rows, "takedowns_landed"), _sum(rows, "takedowns_attempted")),
        "td_def": _defense(_sum(rows, "opp_takedowns_landed"), _sum(rows, "opp_takedowns_attempted")),
        "sub_avg": _per_15(_sum(rows, "sub_attempts"), minutes),
    }


def _row_dict(description: Any, row: Any) -> dict[str, Any]:
    return {column.name: value for column, value in zip(description, row, strict=True)}


def _sum(rows: list[dict[str, Any]], key: str) -> float:
    return float(sum(row[key] for row in rows if row[key] is not None))


def _ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return math.nan
    return numerator / denominator


def _defense(landed_against: float, attempted_against: float) -> float:
    if attempted_against <= 0:
        return math.nan
    return 1 - (landed_against / attempted_against)


def _per_minute(value: float, minutes: float) -> float:
    if math.isnan(minutes) or minutes <= 0:
        return math.nan
    return value / minutes


def _per_15(value: float, minutes: float) -> float:
    if math.isnan(minutes) or minutes <= 0:
        return math.nan
    return (value / minutes) * 15


def _diff(a: float, b: float) -> float:
    if math.isnan(a) or math.isnan(b):
        return math.nan
    return a - b


def _maybe_float(value: Any) -> float:
    if value is None:
        return math.nan
    return float(value)


def _age_years(dob: date | None, fight_date: date) -> float:
    if dob is None:
        return math.nan
    return (fight_date - dob).days / 365.25


def _label(outcome_a: str, outcome_b: str) -> float:
    if outcome_a == "win" and outcome_b == "loss":
        return 1.0
    if outcome_a == "loss" and outcome_b == "win":
        return 0.0
    return math.nan
