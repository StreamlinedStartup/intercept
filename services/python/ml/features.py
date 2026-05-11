"""Point-in-time feature construction for UFC fight prediction."""
from __future__ import annotations

import math
from collections.abc import Sequence
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
    "ufc_fight_count_a",
    "ufc_fight_count_b",
    "ufc_fight_count_diff",
    "ufc_debut",
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
    "weight_class_change",
    "same_weight_class_count_diff",
    "finish_rate_diff",
    "decision_rate_diff",
    "time_in_cage_a",
    "time_in_cage_b",
    "avg_ending_round_diff",
    "decision_tendency_diff",
    "late_round_exposure_diff",
    "common_opponent_count",
    "common_opponent_win_diff",
    "damage_index_a",
    "damage_index_b",
    "stance_orthodox_orthodox",
    "stance_orthodox_southpaw",
    "stance_southpaw_orthodox",
    "stance_southpaw_southpaw",
    "stance_switch_involved",
    "stance_unknown",
]

WEIGHT_CLASS_RECORD_FEATURE_NAMES = [
    "same_weight_class_fight_count_a",
    "same_weight_class_fight_count_b",
    "same_weight_class_fight_count_diff",
    "same_weight_class_win_rate_diff",
    "other_weight_class_win_rate_diff",
    "weight_class_move_lbs_a",
    "weight_class_move_lbs_b",
    "weight_class_move_lbs_diff",
]

EXPERIMENT_FEATURE_NAMES = [*FEATURE_NAMES, *WEIGHT_CLASS_RECORD_FEATURE_NAMES]


def build_features(
    fight_id: str,
    feature_names: Sequence[str] | None = None,
) -> tuple[np.ndarray, float]:
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
                    f.weight_class,
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
            target_weight_class = fighter_a["weight_class"]

    return (
        build_feature_row(
            fighter_a["fighter_id"],
            fighter_b["fighter_id"],
            target_date,
            target_weight_class,
            feature_names=feature_names,
        ),
        _label(fighter_a["outcome"], fighter_b["outcome"]),
    )


def build_feature_row(
    fighter_a_id: str,
    fighter_b_id: str,
    fight_date: date,
    target_weight_class: str | None = None,
    feature_names: Sequence[str] | None = None,
) -> np.ndarray:
    """Build features for a caller-specified fighter order."""
    selected_feature_names = list(feature_names or FEATURE_NAMES)
    feature_values = build_feature_dict(
        fighter_a_id,
        fighter_b_id,
        fight_date,
        target_weight_class,
    )
    unknown = sorted(set(selected_feature_names) - set(feature_values))
    if unknown:
        raise ValueError(f"Unknown feature names: {', '.join(unknown)}")
    return np.array([feature_values[name] for name in selected_feature_names], dtype=float)


def build_feature_dict(
    fighter_a_id: str,
    fighter_b_id: str,
    fight_date: date,
    target_weight_class: str | None = None,
) -> dict[str, float]:
    """Build all known point-in-time feature values keyed by feature name."""
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            fighter_a = _load_fighter(cur, fighter_a_id)
            fighter_b = _load_fighter(cur, fighter_b_id)
            stats_a = _career_stats(cur, fighter_a_id, fight_date)
            stats_b = _career_stats(cur, fighter_b_id, fight_date)
            ufc_fight_count_a = _ufc_fight_count(cur, fighter_a_id, fight_date)
            ufc_fight_count_b = _ufc_fight_count(cur, fighter_b_id, fight_date)
            form_a = _recent_form(cur, fighter_a_id, fight_date)
            form_b = _recent_form(cur, fighter_b_id, fight_date)
            profile_a = _career_profile(cur, fighter_a_id, fight_date, target_weight_class)
            profile_b = _career_profile(cur, fighter_b_id, fight_date, target_weight_class)
            round_tendency_a = _round_tendency_profile(cur, fighter_a_id, fight_date)
            round_tendency_b = _round_tendency_profile(cur, fighter_b_id, fight_date)
            common_opponents = _common_opponent_profile(cur, fighter_a_id, fighter_b_id, fight_date)
            damage_index_a = _damage_index(cur, fighter_a_id, fight_date)
            damage_index_b = _damage_index(cur, fighter_b_id, fight_date)
            weight_record_a = _weight_class_record_profile(
                cur,
                fighter_a_id,
                fight_date,
                target_weight_class,
            )
            weight_record_b = _weight_class_record_profile(
                cur,
                fighter_b_id,
                fight_date,
                target_weight_class,
            )

    stance_features = _stance_one_hot(fighter_a["stance"], fighter_b["stance"])
    feature_values = {
        "slpm_diff": _diff(stats_a["slpm"], stats_b["slpm"]),
        "str_acc_diff": _diff(stats_a["str_acc"], stats_b["str_acc"]),
        "sapm_diff": _diff(stats_a["sapm"], stats_b["sapm"]),
        "str_def_diff": _diff(stats_a["str_def"], stats_b["str_def"]),
        "td_avg_diff": _diff(stats_a["td_avg"], stats_b["td_avg"]),
        "td_acc_diff": _diff(stats_a["td_acc"], stats_b["td_acc"]),
        "td_def_diff": _diff(stats_a["td_def"], stats_b["td_def"]),
        "sub_avg_diff": _diff(stats_a["sub_avg"], stats_b["sub_avg"]),
        "height_diff": _diff(_maybe_float(fighter_a["height_in"]), _maybe_float(fighter_b["height_in"])),
        "reach_diff": _diff(_maybe_float(fighter_a["reach_in"]), _maybe_float(fighter_b["reach_in"])),
        "age_diff": _diff(_age_years(fighter_a["dob"], fight_date), _age_years(fighter_b["dob"], fight_date)),
        "ufc_fight_count_a": float(ufc_fight_count_a),
        "ufc_fight_count_b": float(ufc_fight_count_b),
        "ufc_fight_count_diff": float(ufc_fight_count_a - ufc_fight_count_b),
        "ufc_debut": 1.0 if ufc_fight_count_a == 0 or ufc_fight_count_b == 0 else 0.0,
        "wins_last_3_diff": _diff(form_a["wins_last_3"], form_b["wins_last_3"]),
        "wins_last_5_diff": _diff(form_a["wins_last_5"], form_b["wins_last_5"]),
        "loss_streak_a": form_a["loss_streak"],
        "loss_streak_b": form_b["loss_streak"],
        "coming_off_loss_a": form_a["coming_off_loss"],
        "coming_off_loss_b": form_b["coming_off_loss"],
        "days_since_last_fight_a": form_a["days_since_last_fight"],
        "days_since_last_fight_b": form_b["days_since_last_fight"],
        "days_since_last_fight_diff": _diff(form_a["days_since_last_fight"], form_b["days_since_last_fight"]),
        "long_layoff_a": form_a["long_layoff"],
        "long_layoff_b": form_b["long_layoff"],
        "weight_class_change": _any_true_or_nan(
            profile_a["weight_class_change"],
            profile_b["weight_class_change"],
        ),
        "same_weight_class_count_diff": _diff(
            profile_a["same_weight_class_count"],
            profile_b["same_weight_class_count"],
        ),
        "finish_rate_diff": _diff(profile_a["finish_rate"], profile_b["finish_rate"]),
        "decision_rate_diff": _diff(profile_a["decision_rate"], profile_b["decision_rate"]),
        "time_in_cage_a": profile_a["time_in_cage"],
        "time_in_cage_b": profile_b["time_in_cage"],
        "avg_ending_round_diff": _diff(
            round_tendency_a["avg_ending_round"],
            round_tendency_b["avg_ending_round"],
        ),
        "decision_tendency_diff": _diff(
            round_tendency_a["decision_rate"],
            round_tendency_b["decision_rate"],
        ),
        "late_round_exposure_diff": _diff(
            round_tendency_a["late_exposure_rate"],
            round_tendency_b["late_exposure_rate"],
        ),
        "common_opponent_count": common_opponents["shared_count"],
        "common_opponent_win_diff": common_opponents["win_diff"],
        "damage_index_a": damage_index_a,
        "damage_index_b": damage_index_b,
        "stance_orthodox_orthodox": stance_features[0],
        "stance_orthodox_southpaw": stance_features[1],
        "stance_southpaw_orthodox": stance_features[2],
        "stance_southpaw_southpaw": stance_features[3],
        "stance_switch_involved": stance_features[4],
        "stance_unknown": stance_features[5],
        "same_weight_class_fight_count_a": weight_record_a["same_class_count"],
        "same_weight_class_fight_count_b": weight_record_b["same_class_count"],
        "same_weight_class_fight_count_diff": _diff(
            weight_record_a["same_class_count"],
            weight_record_b["same_class_count"],
        ),
        "same_weight_class_win_rate_diff": _diff(
            weight_record_a["same_class_win_rate"],
            weight_record_b["same_class_win_rate"],
        ),
        "other_weight_class_win_rate_diff": _diff(
            weight_record_a["other_class_win_rate"],
            weight_record_b["other_class_win_rate"],
        ),
        "weight_class_move_lbs_a": weight_record_a["move_lbs"],
        "weight_class_move_lbs_b": weight_record_b["move_lbs"],
        "weight_class_move_lbs_diff": _diff(weight_record_a["move_lbs"], weight_record_b["move_lbs"]),
    }
    return feature_values


def build_decision_signals(
    fighter_a_id: str,
    fighter_b_id: str,
    fight_date: date,
) -> dict[str, Any]:
    """Build operator-facing point-in-time signals for a prediction response."""
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            round_tendency_a = _round_tendency_profile(cur, fighter_a_id, fight_date)
            round_tendency_b = _round_tendency_profile(cur, fighter_b_id, fight_date)
            common_opponents = _common_opponent_profile(cur, fighter_a_id, fighter_b_id, fight_date)
    return {
        "round_tendency": _round_tendency_signal(round_tendency_a, round_tendency_b),
        "common_opponents": _common_opponent_signal(common_opponents),
    }


def _load_fighter(cur: Any, fighter_id: str) -> dict[str, Any]:
    cur.execute(
        """
        SELECT id, dob, height_in, reach_in, stance
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


def _ufc_fight_count(cur: Any, fighter_id: str, target_date: date) -> int:
    cur.execute(
        """
        SELECT COUNT(DISTINCT fr.fight_id)
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        WHERE fr.fighter_id = %s
            AND e.promotion = 'ufc'
            AND e.date < %s
        """,
        (fighter_id, target_date),
    )
    return int(cur.fetchone()[0])


def _recent_form(cur: Any, fighter_id: str, target_date: date) -> dict[str, float]:
    cur.execute(
        """
        SELECT
            fr.outcome,
            e.date AS event_date
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
            AND fr.outcome IN ('win', 'loss')
        ORDER BY e.date DESC, fr.fight_id DESC
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    if not rows:
        return {
            "wins_last_3": math.nan,
            "wins_last_5": math.nan,
            "loss_streak": math.nan,
            "coming_off_loss": math.nan,
            "days_since_last_fight": math.nan,
            "long_layoff": math.nan,
        }

    days_since_last_fight = float((target_date - rows[0]["event_date"]).days)
    return {
        "wins_last_3": float(_wins_in_window(rows, 3)),
        "wins_last_5": float(_wins_in_window(rows, 5)),
        "loss_streak": float(_loss_streak(rows)),
        "coming_off_loss": 1.0 if rows[0]["outcome"] == "loss" else 0.0,
        "days_since_last_fight": days_since_last_fight,
        "long_layoff": 1.0 if days_since_last_fight > 365 else 0.0,
    }


def _wins_in_window(rows: list[dict[str, Any]], window_size: int) -> int:
    return sum(1 for row in rows[:window_size] if row["outcome"] == "win")


def _loss_streak(rows: list[dict[str, Any]]) -> int:
    streak = 0
    for row in rows:
        if row["outcome"] != "loss":
            break
        streak += 1
    return streak


def _career_profile(
    cur: Any,
    fighter_id: str,
    target_date: date,
    target_weight_class: str | None,
) -> dict[str, float]:
    cur.execute(
        """
        SELECT
            fr.outcome,
            fr.method,
            fr.time_seconds,
            f.weight_class,
            e.date AS event_date
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
            AND fr.outcome IN ('win', 'loss')
        ORDER BY e.date DESC, fr.fight_id DESC
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    if not rows:
        return {
            "weight_class_change": math.nan,
            "same_weight_class_count": 0.0 if target_weight_class else math.nan,
            "finish_rate": math.nan,
            "decision_rate": math.nan,
            "time_in_cage": math.nan,
        }

    wins = [row for row in rows if row["outcome"] == "win"]
    time_in_cage = _sum(rows, "time_seconds")
    return {
        "weight_class_change": _weight_class_change(rows, target_weight_class),
        "same_weight_class_count": _same_weight_class_count(rows, target_weight_class),
        "finish_rate": _method_rate(wins, {"ko", "tko", "sub", "submission"}),
        "decision_rate": _method_rate(wins, {"decision"}),
        "time_in_cage": time_in_cage if time_in_cage > 0 else math.nan,
    }


def _weight_class_change(rows: list[dict[str, Any]], target_weight_class: str | None) -> float:
    if target_weight_class is None:
        return math.nan
    recent_weight_class = rows[0]["weight_class"]
    if recent_weight_class is None:
        return math.nan
    return 1.0 if recent_weight_class != target_weight_class else 0.0


def _same_weight_class_count(rows: list[dict[str, Any]], target_weight_class: str | None) -> float:
    if target_weight_class is None:
        return math.nan
    return float(sum(1 for row in rows if row["weight_class"] == target_weight_class))


def _weight_class_record_profile(
    cur: Any,
    fighter_id: str,
    target_date: date,
    target_weight_class: str | None,
) -> dict[str, float]:
    cur.execute(
        """
        SELECT
            fr.outcome,
            f.weight_class,
            e.date AS event_date
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
            AND fr.outcome IN ('win', 'loss')
        ORDER BY e.date DESC, fr.fight_id DESC
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    same_rows = [
        row for row in rows if target_weight_class is not None and row["weight_class"] == target_weight_class
    ]
    other_rows = [
        row for row in rows if target_weight_class is not None and row["weight_class"] != target_weight_class
    ]
    recent_weight_class = rows[0]["weight_class"] if rows else None
    target_limit = _weight_class_limit_lbs(target_weight_class)
    recent_limit = _weight_class_limit_lbs(recent_weight_class)
    return {
        "same_class_count": float(len(same_rows)) if target_weight_class else math.nan,
        "same_class_win_rate": _win_rate(same_rows),
        "other_class_win_rate": _win_rate(other_rows),
        "move_lbs": _diff(target_limit, recent_limit),
    }


def _win_rate(rows: list[dict[str, Any]]) -> float:
    if not rows:
        return math.nan
    return sum(1 for row in rows if row["outcome"] == "win") / len(rows)


def _weight_class_limit_lbs(weight_class: str | None) -> float:
    if weight_class is None:
        return math.nan
    normalized = weight_class.strip().lower()
    for prefix in ["ufc ", "women's ", "womens ", "women "]:
        normalized = normalized.removeprefix(prefix)
    normalized = normalized.removeprefix("interim ")
    normalized = normalized.removeprefix("title ")
    if normalized.startswith("catch") or normalized.startswith("open"):
        return math.nan
    limits = {
        "strawweight": 115.0,
        "flyweight": 125.0,
        "bantamweight": 135.0,
        "featherweight": 145.0,
        "lightweight": 155.0,
        "welterweight": 170.0,
        "middleweight": 185.0,
        "light heavyweight": 205.0,
        "heavyweight": 265.0,
    }
    normalized = normalized.replace(" bout", "").replace(" title", "").strip()
    return limits.get(normalized, math.nan)


def _method_rate(wins: list[dict[str, Any]], method_tokens: set[str]) -> float:
    if not wins:
        return math.nan
    method_wins = sum(1 for row in wins if _method_matches(row["method"], method_tokens))
    return method_wins / len(wins)


def _method_matches(method: str | None, method_tokens: set[str]) -> bool:
    if method is None:
        return False
    normalized = method.strip().lower()
    return any(token in normalized for token in method_tokens)


def _round_tendency_profile(cur: Any, fighter_id: str, target_date: date) -> dict[str, float]:
    cur.execute(
        """
        SELECT
            fr.fight_id,
            fr.method,
            fr.round AS result_round,
            f.scheduled_rounds,
            MAX(frs.round) AS max_stat_round
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        LEFT JOIN fight_round_stats frs
            ON frs.fight_id = fr.fight_id
            AND frs.fighter_id = fr.fighter_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
            AND fr.outcome IN ('win', 'loss')
        GROUP BY fr.fight_id, fr.method, fr.round, f.scheduled_rounds, e.date
        ORDER BY e.date DESC, fr.fight_id DESC
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    endings = [_ending_round(row) for row in rows]
    endings = [ending for ending in endings if not math.isnan(ending)]
    if not endings:
        return {
            "fight_count": 0.0,
            "avg_ending_round": math.nan,
            "decision_rate": math.nan,
            "late_exposure_rate": math.nan,
        }

    decision_count = sum(1 for row in rows if _method_matches(row["method"], {"decision"}))
    late_count = sum(1 for row in rows if _is_late_exposure(row))
    return {
        "fight_count": float(len(endings)),
        "avg_ending_round": sum(endings) / len(endings),
        "decision_rate": decision_count / len(endings),
        "late_exposure_rate": late_count / len(endings),
    }


def _ending_round(row: dict[str, Any]) -> float:
    if row["result_round"] is not None:
        return float(row["result_round"])
    if row["max_stat_round"] is not None:
        return float(row["max_stat_round"])
    return math.nan


def _is_late_exposure(row: dict[str, Any]) -> bool:
    ending_round = _ending_round(row)
    if math.isnan(ending_round):
        return False
    scheduled_rounds = row["scheduled_rounds"]
    if scheduled_rounds is None:
        return ending_round >= 3
    return ending_round >= float(scheduled_rounds)


def _common_opponent_profile(
    cur: Any,
    fighter_a_id: str,
    fighter_b_id: str,
    target_date: date,
) -> dict[str, Any]:
    results_a = _prior_results_by_opponent(cur, fighter_a_id, target_date)
    results_b = _prior_results_by_opponent(cur, fighter_b_id, target_date)
    shared_opponent_ids = sorted(set(results_a) & set(results_b))
    if not shared_opponent_ids:
        return {"shared_count": 0.0, "wins_a": 0.0, "wins_b": 0.0, "win_diff": 0.0}

    wins_a = sum(_wins(results_a[opponent_id]) for opponent_id in shared_opponent_ids)
    wins_b = sum(_wins(results_b[opponent_id]) for opponent_id in shared_opponent_ids)
    return {
        "shared_count": float(len(shared_opponent_ids)),
        "wins_a": float(wins_a),
        "wins_b": float(wins_b),
        "win_diff": float(wins_a - wins_b),
    }


def _prior_results_by_opponent(cur: Any, fighter_id: str, target_date: date) -> dict[str, list[str]]:
    cur.execute(
        """
        SELECT
            fr.opponent_id,
            fr.outcome
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
            AND fr.outcome IN ('win', 'loss')
        """,
        (fighter_id, target_date),
    )
    by_opponent: dict[str, list[str]] = {}
    for row in [_row_dict(cur.description, row) for row in cur.fetchall()]:
        by_opponent.setdefault(row["opponent_id"], []).append(row["outcome"])
    return by_opponent


def _wins(outcomes: list[str]) -> int:
    return sum(1 for outcome in outcomes if outcome == "win")


def _round_tendency_signal(
    profile_a: dict[str, float],
    profile_b: dict[str, float],
) -> dict[str, Any]:
    if profile_a["fight_count"] < 2 or profile_b["fight_count"] < 2:
        return {
            "label": "Thin history",
            "summary": "Not enough prior UFC round data for both fighters.",
            "advantage": "neutral",
        }

    late_diff = _diff(profile_a["late_exposure_rate"], profile_b["late_exposure_rate"])
    decision_diff = _diff(profile_a["decision_rate"], profile_b["decision_rate"])
    avg_round_diff = _diff(profile_a["avg_ending_round"], profile_b["avg_ending_round"])
    if any(math.isnan(value) for value in [late_diff, decision_diff, avg_round_diff]):
        return {
            "label": "Thin history",
            "summary": "Prior round data is incomplete for this matchup.",
            "advantage": "neutral",
        }

    combined = (late_diff + decision_diff + (avg_round_diff / 5.0)) / 3.0
    if abs(combined) < 0.15:
        return {
            "label": "Mixed history",
            "summary": "Prior round profiles do not clearly favor either fighter.",
            "advantage": "neutral",
        }

    if combined > 0:
        return {
            "label": "Late/decision lean",
            "summary": "Fighter A has more prior late-fight and decision exposure.",
            "advantage": "fighter_a",
        }

    return {
        "label": "Late/decision lean",
        "summary": "Fighter B has more prior late-fight and decision exposure.",
        "advantage": "fighter_b",
    }


def _common_opponent_signal(profile: dict[str, Any]) -> dict[str, Any]:
    shared_count = int(profile["shared_count"])
    if shared_count == 0:
        return {
            "label": "No shared opponents",
            "summary": "No shared prior opponents before this fight date.",
            "advantage": "neutral",
        }

    wins_a = int(profile["wins_a"])
    wins_b = int(profile["wins_b"])
    if wins_a == wins_b:
        return {
            "label": "Split shared history",
            "summary": f"Both fighters are {wins_a}-{shared_count - wins_a} against shared opponents.",
            "advantage": "neutral",
        }

    if wins_a > wins_b:
        return {
            "label": "A stronger vs shared opponents",
            "summary": f"Fighter A is {wins_a}-{shared_count - wins_a}; Fighter B is {wins_b}-{shared_count - wins_b}.",
            "advantage": "fighter_a",
        }

    return {
        "label": "B stronger vs shared opponents",
        "summary": f"Fighter B is {wins_b}-{shared_count - wins_b}; Fighter A is {wins_a}-{shared_count - wins_a}.",
        "advantage": "fighter_b",
    }


def _any_true_or_nan(a: float, b: float) -> float:
    values = [value for value in [a, b] if not math.isnan(value)]
    if not values:
        return math.nan
    return 1.0 if any(value == 1.0 for value in values) else 0.0


def _damage_index(cur: Any, fighter_id: str, target_date: date) -> float:
    cur.execute(
        """
        SELECT
            fr.outcome,
            fr.method,
            opp.method AS opp_method,
            opp.sig_strikes_landed AS sig_strikes_absorbed
        FROM fight_results fr
        JOIN fights f ON f.id = fr.fight_id
        JOIN events e ON e.id = f.event_id
        LEFT JOIN fight_results opp
            ON opp.fight_id = fr.fight_id
            AND opp.fighter_id = fr.opponent_id
        WHERE fr.fighter_id = %s
            AND e.date < %s
        ORDER BY e.date DESC, fr.fight_id DESC
        LIMIT 3
        """,
        (fighter_id, target_date),
    )
    rows = [_row_dict(cur.description, row) for row in cur.fetchall()]
    if not rows:
        return math.nan

    total = 0.0
    has_absorbed = False
    for row in rows:
        absorbed = row["sig_strikes_absorbed"]
        if absorbed is None:
            continue
        has_absorbed = True
        multiplier = 2.0 if _is_ko_tko_loss(row) else 1.0
        total += float(absorbed) * multiplier
    return total if has_absorbed else math.nan


def _is_ko_tko_loss(row: dict[str, Any]) -> bool:
    if row["outcome"] != "loss":
        return False
    return _method_matches(row["method"], {"ko", "tko"}) or _method_matches(
        row["opp_method"],
        {"ko", "tko"},
    )


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


def _stance_one_hot(stance_a: str | None, stance_b: str | None) -> list[float]:
    stance_match = _stance_match(stance_a, stance_b)
    categories = [
        "orthodox_orthodox",
        "orthodox_southpaw",
        "southpaw_orthodox",
        "southpaw_southpaw",
        "switch_involved",
        "unknown",
    ]
    return [1.0 if stance_match == category else 0.0 for category in categories]


def _stance_match(stance_a: str | None, stance_b: str | None) -> str:
    normalized_a = _normalize_stance(stance_a)
    normalized_b = _normalize_stance(stance_b)
    if normalized_a is None or normalized_b is None:
        return "unknown"
    if normalized_a == "switch" or normalized_b == "switch":
        return "switch_involved"
    if normalized_a in {"orthodox", "southpaw"} and normalized_b in {"orthodox", "southpaw"}:
        return f"{normalized_a}_{normalized_b}"
    return "unknown"


def _normalize_stance(stance: str | None) -> str | None:
    if stance is None:
        return None
    normalized = stance.strip().lower()
    if normalized in {"orthodox", "southpaw", "switch"}:
        return normalized
    return None
