"""Tests for UFC Fight Predictor ML feature construction."""
from __future__ import annotations

import math
import os
import sys
from datetime import date
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL is required for database-backed ML tests",
)

sys.path.insert(0, str(Path(__file__).parent))

from ml.db import pool
from ml.experiments import rank_variant_results
from ml.features import (
    FEATURE_NAMES,
    WEIGHT_CLASS_RECORD_FEATURE_NAMES,
    build_decision_signals,
    build_feature_row,
    build_features,
)


def test_no_leakage() -> None:
    """Later fights for a fighter must not affect earlier fight features."""
    prefix = "test-pcuc-leakage"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix)
        conn.commit()

    early_features, early_label = build_features(f"{prefix}-target-early")
    late_features, late_label = build_features(f"{prefix}-target-late")

    slpm_index = FEATURE_NAMES.index("slpm_diff")
    height_index = FEATURE_NAMES.index("height_diff")
    reach_index = FEATURE_NAMES.index("reach_diff")

    assert math.isnan(early_features[slpm_index])
    assert early_features[height_index] == pytest.approx(2.0)
    assert early_features[reach_index] == pytest.approx(1.0)
    assert early_label == 1.0

    assert late_features[slpm_index] == pytest.approx(3.0)
    assert late_label == 0.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_stance_direction_is_asymmetric() -> None:
    prefix = "test-pcuc-stance"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix, alpha_stance="orthodox", beta_stance="southpaw")
        conn.commit()

    features, _label = build_features(f"{prefix}-target-early")

    orthodox_southpaw = FEATURE_NAMES.index("stance_orthodox_southpaw")
    southpaw_orthodox = FEATURE_NAMES.index("stance_southpaw_orthodox")
    assert features[orthodox_southpaw] == 1.0
    assert features[southpaw_orthodox] == 0.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_ufc_debut_for_fighter_with_zero_prior_ufc_fights() -> None:
    prefix = "test-n40x-debut"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target-early")

    count_a = FEATURE_NAMES.index("ufc_fight_count_a")
    count_b = FEATURE_NAMES.index("ufc_fight_count_b")
    count_diff = FEATURE_NAMES.index("ufc_fight_count_diff")
    debut = FEATURE_NAMES.index("ufc_debut")

    assert features[count_a] == 0.0
    assert features[count_b] == 0.0
    assert features[count_diff] == 0.0
    assert features[debut] == 1.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_non_ufc_prior_fight_does_not_increment_ufc_fight_count() -> None:
    prefix = "test-n40x-non-ufc"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_non_ufc_experience_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")

    count_a = FEATURE_NAMES.index("ufc_fight_count_a")
    count_b = FEATURE_NAMES.index("ufc_fight_count_b")
    debut = FEATURE_NAMES.index("ufc_debut")

    assert features[count_a] == 0.0
    assert features[count_b] == 0.0
    assert features[debut] == 1.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_recent_form_counts_wins_in_last_five() -> None:
    prefix = "test-palv-form"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_recent_form_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")

    wins_last_3_diff = FEATURE_NAMES.index("wins_last_3_diff")
    wins_last_5_diff = FEATURE_NAMES.index("wins_last_5_diff")
    loss_streak_a = FEATURE_NAMES.index("loss_streak_a")
    coming_off_loss_a = FEATURE_NAMES.index("coming_off_loss_a")
    days_since_last_fight_a = FEATURE_NAMES.index("days_since_last_fight_a")
    long_layoff_a = FEATURE_NAMES.index("long_layoff_a")

    assert features[wins_last_3_diff] == 2.0
    assert features[wins_last_5_diff] == 3.0
    assert features[loss_streak_a] == 0.0
    assert features[coming_off_loss_a] == 0.0
    assert features[days_since_last_fight_a] == 31.0
    assert features[long_layoff_a] == 0.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_recent_form_features_are_nan_without_prior_fights() -> None:
    prefix = "test-palv-no-form"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target-early")

    form_feature_names = [
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
    ]
    for feature_name in form_feature_names:
        assert math.isnan(features[FEATURE_NAMES.index(feature_name)])

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_weight_class_change_after_three_lightweight_fights_then_welterweight() -> None:
    prefix = "test-nk4h-weight"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_weight_class_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")

    weight_class_change = FEATURE_NAMES.index("weight_class_change")
    same_weight_class_count_diff = FEATURE_NAMES.index("same_weight_class_count_diff")
    finish_rate_diff = FEATURE_NAMES.index("finish_rate_diff")
    decision_rate_diff = FEATURE_NAMES.index("decision_rate_diff")
    time_in_cage_a = FEATURE_NAMES.index("time_in_cage_a")
    time_in_cage_b = FEATURE_NAMES.index("time_in_cage_b")
    damage_index_a = FEATURE_NAMES.index("damage_index_a")
    damage_index_b = FEATURE_NAMES.index("damage_index_b")

    assert features[weight_class_change] == 1.0
    assert features[same_weight_class_count_diff] == -1.0
    assert features[finish_rate_diff] == pytest.approx(0.5)
    assert features[decision_rate_diff] == pytest.approx(-0.5)
    assert features[time_in_cage_a] == 900.0
    assert features[time_in_cage_b] == 300.0
    assert features[damage_index_a] == 60.0
    assert features[damage_index_b] == 10.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_weight_class_record_features_use_only_prior_fights() -> None:
    prefix = "test-fv-weight-prior"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_weight_class_record_fixture(cur, prefix)
        conn.commit()

    feature_names = list(WEIGHT_CLASS_RECORD_FEATURE_NAMES)
    features = build_feature_row(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-05-01"),
        "welterweight",
        feature_names=feature_names,
    )

    values = dict(zip(feature_names, features, strict=True))
    assert values["same_weight_class_fight_count_a"] == 1.0
    assert values["same_weight_class_fight_count_b"] == 2.0
    assert values["same_weight_class_fight_count_diff"] == -1.0
    assert values["same_weight_class_win_rate_diff"] == pytest.approx(0.5)
    assert values["other_weight_class_win_rate_diff"] == pytest.approx(1.0)
    assert values["weight_class_move_lbs_a"] == 0.0
    assert values["weight_class_move_lbs_b"] == 15.0
    assert values["weight_class_move_lbs_diff"] == -15.0

    middleweight_features = build_feature_row(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-05-01"),
        "middleweight",
        feature_names=feature_names,
    )
    middleweight_values = dict(zip(feature_names, middleweight_features, strict=True))
    assert middleweight_values["same_weight_class_fight_count_a"] == 0.0
    assert middleweight_values["same_weight_class_fight_count_b"] == 0.0
    assert math.isnan(middleweight_values["same_weight_class_win_rate_diff"])
    assert middleweight_values["weight_class_move_lbs_a"] == 15.0
    assert middleweight_values["weight_class_move_lbs_b"] == 30.0

    future_features = build_feature_row(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-07-01"),
        "welterweight",
        feature_names=feature_names,
    )
    future_values = dict(zip(feature_names, future_features, strict=True))
    assert future_values["same_weight_class_fight_count_a"] == 3.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_weight_class_record_features_keep_odd_labels_but_nan_move_lbs() -> None:
    prefix = "test-fv-catch"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_catch_weight_fixture(cur, prefix)
        conn.commit()

    feature_names = list(WEIGHT_CLASS_RECORD_FEATURE_NAMES)
    features = build_feature_row(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-03-01"),
        "catch weight",
        feature_names=feature_names,
    )
    values = dict(zip(feature_names, features, strict=True))

    assert values["same_weight_class_fight_count_a"] == 1.0
    assert values["same_weight_class_fight_count_b"] == 1.0
    assert math.isnan(values["weight_class_move_lbs_a"])
    assert math.isnan(values["weight_class_move_lbs_b"])
    assert math.isnan(values["weight_class_move_lbs_diff"])

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_feature_variant_vectors_stay_length_aligned() -> None:
    prefix = "test-fv-align"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(
        f"{prefix}-target-early",
        feature_names=[*FEATURE_NAMES, *WEIGHT_CLASS_RECORD_FEATURE_NAMES],
    )

    assert len(features) == len(FEATURE_NAMES) + len(WEIGHT_CLASS_RECORD_FEATURE_NAMES)

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_variant_ranking_prefers_log_loss_before_accuracy() -> None:
    ranked = rank_variant_results(
        [
            {
                "variant": "higher_accuracy",
                "overall": {
                    "log_loss": 0.70,
                    "brier_score": 0.20,
                    "abs_calibration_error": 0.01,
                    "roc_auc": 0.90,
                    "accuracy": 0.90,
                },
            },
            {
                "variant": "lower_log_loss",
                "overall": {
                    "log_loss": 0.60,
                    "brier_score": 0.25,
                    "abs_calibration_error": 0.10,
                    "roc_auc": 0.60,
                    "accuracy": 0.55,
                },
            },
        ]
    )

    assert [row["variant"] for row in ranked] == ["lower_log_loss", "higher_accuracy"]


def test_round_tendency_uses_only_prior_round_stats() -> None:
    prefix = "test-x1vw-round"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_round_tendency_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")
    signals = build_decision_signals(
        f"{prefix}-alpha",
        f"{prefix}-gamma",
        date.fromisoformat("2020-04-01"),
    )

    avg_ending_round_diff = FEATURE_NAMES.index("avg_ending_round_diff")
    decision_tendency_diff = FEATURE_NAMES.index("decision_tendency_diff")
    late_round_exposure_diff = FEATURE_NAMES.index("late_round_exposure_diff")

    assert features[avg_ending_round_diff] == pytest.approx(2.0)
    assert features[decision_tendency_diff] == pytest.approx(1.0)
    assert features[late_round_exposure_diff] == pytest.approx(1.0)
    assert signals["round_tendency"]["label"] == "Late/decision lean"
    assert signals["round_tendency"]["advantage"] == "fighter_a"

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_common_opponent_features_compare_shared_prior_results() -> None:
    prefix = "test-c483-common"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_common_opponent_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")
    signals = build_decision_signals(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-04-01"),
    )

    common_opponent_count = FEATURE_NAMES.index("common_opponent_count")
    common_opponent_win_diff = FEATURE_NAMES.index("common_opponent_win_diff")

    assert features[common_opponent_count] == 2.0
    assert features[common_opponent_win_diff] == 1.0
    assert signals["common_opponents"]["label"] == "A stronger vs shared opponents"
    assert signals["common_opponents"]["advantage"] == "fighter_a"

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_common_opponent_features_ignore_future_shared_results() -> None:
    prefix = "test-c483-future"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_common_opponent_fixture(cur, prefix)
        conn.commit()

    features, _label = build_features(f"{prefix}-target")

    common_opponent_count = FEATURE_NAMES.index("common_opponent_count")
    common_opponent_win_diff = FEATURE_NAMES.index("common_opponent_win_diff")

    assert features[common_opponent_count] == 2.0
    assert features[common_opponent_win_diff] == 1.0

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def test_common_opponent_signal_handles_no_shared_opponents() -> None:
    prefix = "test-c483-none"
    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
            _insert_fixture(cur, prefix)
        conn.commit()

    signals = build_decision_signals(
        f"{prefix}-alpha",
        f"{prefix}-beta",
        date.fromisoformat("2020-01-01"),
    )

    assert signals["common_opponents"]["label"] == "No shared opponents"
    assert signals["common_opponents"]["advantage"] == "neutral"

    with pool.borrow() as conn:
        with conn.cursor() as cur:
            _delete_fixture(cur, prefix)
        conn.commit()


def _delete_fixture(cur, prefix: str) -> None:
    cur.execute("DELETE FROM fight_round_stats WHERE fight_id LIKE %s", (f"{prefix}-%",))
    cur.execute("DELETE FROM fight_results WHERE fight_id LIKE %s", (f"{prefix}-%",))
    cur.execute("DELETE FROM fights WHERE id LIKE %s", (f"{prefix}-%",))
    cur.execute("DELETE FROM events WHERE id LIKE %s", (f"{prefix}-%",))
    cur.execute("DELETE FROM fighters WHERE id LIKE %s", (f"{prefix}-%",))


def _insert_fixture(
    cur,
    prefix: str,
    *,
    alpha_stance: str | None = None,
    beta_stance: str | None = None,
) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, %s),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, %s)
        """,
        (f"{prefix}-alpha", alpha_stance, f"{prefix}-beta", beta_stance),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Fixture Target Early', '2020-01-01', true, 'ufc'),
            (%s, 'Fixture Prior After Early', '2020-02-01', true, 'ufc'),
            (%s, 'Fixture Target Late', '2020-03-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-early",
            f"{prefix}-event-prior-after-early",
            f"{prefix}-event-late",
        ),
    )
    cur.execute(
        """
        INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
        VALUES
            (%s, %s, 'welterweight', 3, false),
            (%s, %s, 'welterweight', 3, false),
            (%s, %s, 'welterweight', 3, false)
        """,
        (
            f"{prefix}-target-early",
            f"{prefix}-event-early",
            f"{prefix}-prior-after-early",
            f"{prefix}-event-prior-after-early",
            f"{prefix}-target-late",
            f"{prefix}-event-late",
        ),
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-target-early",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=1,
        beta_sig_landed=1,
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-prior-after-early",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=40,
        beta_sig_landed=10,
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-target-late",
        alpha_outcome="loss",
        beta_outcome="win",
        alpha_sig_landed=1,
        beta_sig_landed=1,
    )


def _insert_weight_class_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null),
            (%s, 'Fixture Gamma', '1991-01-01', 71, 72, null),
            (%s, 'Fixture Delta', '1993-01-01', 69, 71, null)
        """,
        (
            f"{prefix}-alpha",
            f"{prefix}-beta",
            f"{prefix}-gamma",
            f"{prefix}-delta",
        ),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Fixture Lightweight 1', '2020-01-01', true, 'ufc'),
            (%s, 'Fixture Lightweight 2', '2020-02-01', true, 'ufc'),
            (%s, 'Fixture Lightweight 3', '2020-03-01', true, 'ufc'),
            (%s, 'Fixture Welterweight Prior', '2020-04-01', true, 'ufc'),
            (%s, 'Fixture Welterweight Target', '2020-05-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-lightweight-1",
            f"{prefix}-event-lightweight-2",
            f"{prefix}-event-lightweight-3",
            f"{prefix}-event-welterweight-prior",
            f"{prefix}-event-target",
        ),
    )
    for index in range(1, 4):
        cur.execute(
            """
            INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
            VALUES (%s, %s, 'lightweight', 3, false)
            """,
            (f"{prefix}-lightweight-{index}", f"{prefix}-event-lightweight-{index}"),
        )
    cur.execute(
        """
        INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
        VALUES
            (%s, %s, 'welterweight', 3, false),
            (%s, %s, 'welterweight', 3, false)
        """,
        (
            f"{prefix}-welterweight-prior",
            f"{prefix}-event-welterweight-prior",
            f"{prefix}-target",
            f"{prefix}-event-target",
        ),
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-lightweight-1",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-beta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
        fighter_a_method="KO/TKO",
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-lightweight-2",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-beta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
        fighter_a_method="Decision - Unanimous",
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-lightweight-3",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-beta",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=10,
        fighter_b_sig_landed=20,
        fighter_b_method="KO/TKO",
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-welterweight-prior",
        fighter_a_id=f"{prefix}-gamma",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
        fighter_a_method="Decision - Split",
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-target",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
        fighter_a_method="Decision - Unanimous",
    )


def _insert_weight_class_record_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null),
            (%s, 'Fixture Gamma', '1991-01-01', 71, 72, null),
            (%s, 'Fixture Delta', '1993-01-01', 69, 71, null)
        """,
        (
            f"{prefix}-alpha",
            f"{prefix}-beta",
            f"{prefix}-gamma",
            f"{prefix}-delta",
        ),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Alpha Lightweight', '2020-01-01', true, 'ufc'),
            (%s, 'Alpha Welterweight', '2020-02-01', true, 'ufc'),
            (%s, 'Beta Welterweight 1', '2020-01-15', true, 'ufc'),
            (%s, 'Beta Welterweight 2', '2020-02-15', true, 'ufc'),
            (%s, 'Beta Lightweight', '2020-03-01', true, 'ufc'),
            (%s, 'Target', '2020-05-01', true, 'ufc'),
            (%s, 'Future Alpha Welterweight', '2020-06-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-alpha-lightweight",
            f"{prefix}-event-alpha-welterweight",
            f"{prefix}-event-beta-welterweight-1",
            f"{prefix}-event-beta-welterweight-2",
            f"{prefix}-event-beta-lightweight",
            f"{prefix}-event-target",
            f"{prefix}-event-future",
        ),
    )
    fights = [
        (f"{prefix}-alpha-lightweight", f"{prefix}-event-alpha-lightweight", "lightweight"),
        (f"{prefix}-alpha-welterweight", f"{prefix}-event-alpha-welterweight", "welterweight"),
        (f"{prefix}-beta-welterweight-1", f"{prefix}-event-beta-welterweight-1", "welterweight"),
        (f"{prefix}-beta-welterweight-2", f"{prefix}-event-beta-welterweight-2", "welterweight"),
        (f"{prefix}-beta-lightweight", f"{prefix}-event-beta-lightweight", "lightweight"),
        (f"{prefix}-target", f"{prefix}-event-target", "welterweight"),
        (f"{prefix}-future", f"{prefix}-event-future", "welterweight"),
    ]
    for fight_id, event_id, weight_class in fights:
        cur.execute(
            """
            INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
            VALUES (%s, %s, %s, 3, false)
            """,
            (fight_id, event_id, weight_class),
        )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-alpha-lightweight",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-alpha-welterweight",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-beta-welterweight-1",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-beta-welterweight-2",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=10,
        fighter_b_sig_landed=20,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-beta-lightweight",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=10,
        fighter_b_sig_landed=20,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-target",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-beta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-future",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=10,
        fighter_b_sig_landed=20,
    )


def _insert_catch_weight_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null)
        """,
        (f"{prefix}-alpha", f"{prefix}-beta"),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Catch Prior', '2020-01-01', true, 'ufc'),
            (%s, 'Target', '2020-03-01', true, 'ufc')
        """,
        (f"{prefix}-event-prior", f"{prefix}-event-target"),
    )
    cur.execute(
        """
        INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
        VALUES
            (%s, %s, 'catch weight', 3, false),
            (%s, %s, 'catch weight', 3, false)
        """,
        (
            f"{prefix}-prior",
            f"{prefix}-event-prior",
            f"{prefix}-target",
            f"{prefix}-event-target",
        ),
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-prior",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=20,
        beta_sig_landed=10,
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-target",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=1,
        beta_sig_landed=1,
    )


def _insert_round_tendency_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null),
            (%s, 'Fixture Gamma', '1991-01-01', 71, 72, null),
            (%s, 'Fixture Delta', '1993-01-01', 69, 71, null)
        """,
        (
            f"{prefix}-alpha",
            f"{prefix}-beta",
            f"{prefix}-gamma",
            f"{prefix}-delta",
        ),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Fixture Alpha Decision 1', '2020-01-01', true, 'ufc'),
            (%s, 'Fixture Alpha Decision 2', '2020-02-01', true, 'ufc'),
            (%s, 'Fixture Gamma Early 1', '2020-01-15', true, 'ufc'),
            (%s, 'Fixture Gamma Early 2', '2020-02-15', true, 'ufc'),
            (%s, 'Fixture Target', '2020-04-01', true, 'ufc'),
            (%s, 'Fixture Future Noise', '2020-05-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-alpha-decision-1",
            f"{prefix}-event-alpha-decision-2",
            f"{prefix}-event-gamma-early-1",
            f"{prefix}-event-gamma-early-2",
            f"{prefix}-event-target",
            f"{prefix}-event-future-noise",
        ),
    )
    fights = [
        (f"{prefix}-alpha-decision-1", f"{prefix}-event-alpha-decision-1"),
        (f"{prefix}-alpha-decision-2", f"{prefix}-event-alpha-decision-2"),
        (f"{prefix}-gamma-early-1", f"{prefix}-event-gamma-early-1"),
        (f"{prefix}-gamma-early-2", f"{prefix}-event-gamma-early-2"),
        (f"{prefix}-target", f"{prefix}-event-target"),
        (f"{prefix}-future-noise", f"{prefix}-event-future-noise"),
    ]
    for fight_id, event_id in fights:
        cur.execute(
            """
            INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
            VALUES (%s, %s, 'welterweight', 3, false)
            """,
            (fight_id, event_id),
        )
    for fight_id in [f"{prefix}-alpha-decision-1", f"{prefix}-alpha-decision-2"]:
        _insert_result_pair_for_fighters(
            cur,
            fight_id=fight_id,
            fighter_a_id=f"{prefix}-alpha",
            fighter_b_id=f"{prefix}-beta",
            fighter_a_outcome="win",
            fighter_b_outcome="loss",
            fighter_a_sig_landed=30,
            fighter_b_sig_landed=20,
            fighter_a_method="Decision - Unanimous",
            fighter_a_round=3,
            fighter_b_round=3,
        )
        _insert_round_rows(cur, fight_id, f"{prefix}-alpha", 3)
        _insert_round_rows(cur, fight_id, f"{prefix}-beta", 3)
    for fight_id in [f"{prefix}-gamma-early-1", f"{prefix}-gamma-early-2"]:
        _insert_result_pair_for_fighters(
            cur,
            fight_id=fight_id,
            fighter_a_id=f"{prefix}-gamma",
            fighter_b_id=f"{prefix}-delta",
            fighter_a_outcome="win",
            fighter_b_outcome="loss",
            fighter_a_sig_landed=10,
            fighter_b_sig_landed=5,
            fighter_a_method="KO/TKO",
            fighter_a_round=1,
            fighter_b_round=1,
        )
        _insert_round_rows(cur, fight_id, f"{prefix}-gamma", 1)
        _insert_round_rows(cur, fight_id, f"{prefix}-delta", 1)
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-target",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-future-noise",
        fighter_a_id=f"{prefix}-gamma",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=40,
        fighter_b_sig_landed=10,
        fighter_a_method="Decision - Unanimous",
        fighter_a_round=3,
        fighter_b_round=3,
    )
    _insert_round_rows(cur, f"{prefix}-future-noise", f"{prefix}-gamma", 3)
    _insert_round_rows(cur, f"{prefix}-future-noise", f"{prefix}-delta", 3)


def _insert_common_opponent_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null),
            (%s, 'Fixture Shared One', '1991-01-01', 71, 72, null),
            (%s, 'Fixture Shared Two', '1993-01-01', 69, 71, null)
        """,
        (
            f"{prefix}-alpha",
            f"{prefix}-beta",
            f"{prefix}-shared-one",
            f"{prefix}-shared-two",
        ),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Alpha Shared One', '2020-01-01', true, 'ufc'),
            (%s, 'Alpha Shared Two', '2020-02-01', true, 'ufc'),
            (%s, 'Beta Shared One', '2020-01-15', true, 'ufc'),
            (%s, 'Beta Shared Two', '2020-02-15', true, 'ufc'),
            (%s, 'Target', '2020-04-01', true, 'ufc'),
            (%s, 'Future Shared Noise', '2020-05-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-alpha-shared-one",
            f"{prefix}-event-alpha-shared-two",
            f"{prefix}-event-beta-shared-one",
            f"{prefix}-event-beta-shared-two",
            f"{prefix}-event-target",
            f"{prefix}-event-future-noise",
        ),
    )
    fights = [
        (f"{prefix}-alpha-shared-one", f"{prefix}-event-alpha-shared-one"),
        (f"{prefix}-alpha-shared-two", f"{prefix}-event-alpha-shared-two"),
        (f"{prefix}-beta-shared-one", f"{prefix}-event-beta-shared-one"),
        (f"{prefix}-beta-shared-two", f"{prefix}-event-beta-shared-two"),
        (f"{prefix}-target", f"{prefix}-event-target"),
        (f"{prefix}-future-noise", f"{prefix}-event-future-noise"),
    ]
    for fight_id, event_id in fights:
        cur.execute(
            """
            INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
            VALUES (%s, %s, 'welterweight', 3, false)
            """,
            (fight_id, event_id),
        )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-alpha-shared-one",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-shared-one",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-alpha-shared-two",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-shared-two",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-beta-shared-one",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-shared-one",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=10,
        fighter_b_sig_landed=20,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-beta-shared-two",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-shared-two",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=20,
        fighter_b_sig_landed=10,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-target",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-beta",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-future-noise",
        fighter_a_id=f"{prefix}-beta",
        fighter_b_id=f"{prefix}-shared-one",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=40,
        fighter_b_sig_landed=10,
    )


def _insert_recent_form_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null),
            (%s, 'Fixture Gamma', '1991-01-01', 71, 72, null),
            (%s, 'Fixture Delta', '1993-01-01', 69, 71, null)
        """,
        (
            f"{prefix}-alpha",
            f"{prefix}-beta",
            f"{prefix}-gamma",
            f"{prefix}-delta",
        ),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Fixture Prior 1', '2020-01-01', true, 'ufc'),
            (%s, 'Fixture Prior 2', '2020-02-01', true, 'ufc'),
            (%s, 'Fixture Prior 3', '2020-03-01', true, 'ufc'),
            (%s, 'Fixture Prior 4', '2020-04-01', true, 'ufc'),
            (%s, 'Fixture Prior 5', '2020-05-01', true, 'ufc'),
            (%s, 'Fixture Opponent Prior', '2020-05-15', true, 'ufc'),
            (%s, 'Fixture Target', '2020-06-01', true, 'ufc')
        """,
        (
            f"{prefix}-event-prior-1",
            f"{prefix}-event-prior-2",
            f"{prefix}-event-prior-3",
            f"{prefix}-event-prior-4",
            f"{prefix}-event-prior-5",
            f"{prefix}-event-opponent-prior",
            f"{prefix}-event-target",
        ),
    )
    for index in range(1, 6):
        cur.execute(
            """
            INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
            VALUES (%s, %s, 'welterweight', 3, false)
            """,
            (f"{prefix}-prior-{index}", f"{prefix}-event-prior-{index}"),
        )
    cur.execute(
        """
        INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
        VALUES
            (%s, %s, 'welterweight', 3, false),
            (%s, %s, 'welterweight', 3, false)
        """,
        (
            f"{prefix}-opponent-prior",
            f"{prefix}-event-opponent-prior",
            f"{prefix}-target",
            f"{prefix}-event-target",
        ),
    )

    alpha_outcomes = ["win", "loss", "win", "loss", "win"]
    for index, alpha_outcome in enumerate(alpha_outcomes, start=1):
        beta_outcome = "loss" if alpha_outcome == "win" else "win"
        _insert_result_pair_for_fighters(
            cur,
            fight_id=f"{prefix}-prior-{index}",
            fighter_a_id=f"{prefix}-alpha",
            fighter_b_id=f"{prefix}-beta",
            fighter_a_outcome=alpha_outcome,
            fighter_b_outcome=beta_outcome,
            fighter_a_sig_landed=20,
            fighter_b_sig_landed=10,
        )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-target",
        fighter_a_id=f"{prefix}-alpha",
        fighter_b_id=f"{prefix}-gamma",
        fighter_a_outcome="win",
        fighter_b_outcome="loss",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
    )
    _insert_result_pair_for_fighters(
        cur,
        fight_id=f"{prefix}-opponent-prior",
        fighter_a_id=f"{prefix}-gamma",
        fighter_b_id=f"{prefix}-delta",
        fighter_a_outcome="loss",
        fighter_b_outcome="win",
        fighter_a_sig_landed=1,
        fighter_b_sig_landed=1,
    )


def _insert_non_ufc_experience_fixture(cur, prefix: str) -> None:
    cur.execute(
        """
        INSERT INTO fighters (id, name, dob, height_in, reach_in, stance)
        VALUES
            (%s, 'Fixture Alpha', '1990-01-01', 72, 74, null),
            (%s, 'Fixture Beta', '1992-01-01', 70, 73, null)
        """,
        (f"{prefix}-alpha", f"{prefix}-beta"),
    )
    cur.execute(
        """
        INSERT INTO events (id, name, date, completed, promotion)
        VALUES
            (%s, 'Fixture Prior Bellator', '2020-01-01', true, 'bellator'),
            (%s, 'Fixture Target UFC', '2020-02-01', true, 'ufc')
        """,
        (f"{prefix}-event-prior-bellator", f"{prefix}-event-target"),
    )
    cur.execute(
        """
        INSERT INTO fights (id, event_id, weight_class, scheduled_rounds, is_headliner)
        VALUES
            (%s, %s, 'welterweight', 3, false),
            (%s, %s, 'welterweight', 3, false)
        """,
        (
            f"{prefix}-prior-bellator",
            f"{prefix}-event-prior-bellator",
            f"{prefix}-target",
            f"{prefix}-event-target",
        ),
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-prior-bellator",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=40,
        beta_sig_landed=10,
    )
    _insert_result_pair(
        cur,
        prefix,
        fight_id=f"{prefix}-target",
        alpha_outcome="win",
        beta_outcome="loss",
        alpha_sig_landed=1,
        beta_sig_landed=1,
    )


def _insert_result_pair(
    cur,
    prefix: str,
    *,
    fight_id: str,
    alpha_outcome: str,
    beta_outcome: str,
    alpha_sig_landed: int,
    beta_sig_landed: int,
) -> None:
    cur.execute(
        """
        INSERT INTO fight_results (
            fight_id,
            fighter_id,
            opponent_id,
            outcome,
            time_seconds,
            sig_strikes_landed,
            sig_strikes_attempted,
            takedowns_landed,
            takedowns_attempted,
            sub_attempts
        )
        VALUES
            (%s, %s, %s, %s, 300, %s, 50, 1, 2, 0),
            (%s, %s, %s, %s, 300, %s, 50, 0, 1, 0)
        """,
        (
            fight_id,
            f"{prefix}-alpha",
            f"{prefix}-beta",
            alpha_outcome,
            alpha_sig_landed,
            fight_id,
            f"{prefix}-beta",
            f"{prefix}-alpha",
            beta_outcome,
            beta_sig_landed,
        ),
    )


def _insert_result_pair_for_fighters(
    cur,
    *,
    fight_id: str,
    fighter_a_id: str,
    fighter_b_id: str,
    fighter_a_outcome: str,
    fighter_b_outcome: str,
    fighter_a_sig_landed: int,
    fighter_b_sig_landed: int,
    fighter_a_method: str | None = None,
    fighter_b_method: str | None = None,
    fighter_a_round: int | None = None,
    fighter_b_round: int | None = None,
) -> None:
    cur.execute(
        """
        INSERT INTO fight_results (
            fight_id,
            fighter_id,
            opponent_id,
            outcome,
            method,
            round,
            time_seconds,
            sig_strikes_landed,
            sig_strikes_attempted,
            takedowns_landed,
            takedowns_attempted,
            sub_attempts
        )
        VALUES
            (%s, %s, %s, %s, %s, %s, 300, %s, 50, 1, 2, 0),
            (%s, %s, %s, %s, %s, %s, 300, %s, 50, 0, 1, 0)
        """,
        (
            fight_id,
            fighter_a_id,
            fighter_b_id,
            fighter_a_outcome,
            fighter_a_method,
            fighter_a_round,
            fighter_a_sig_landed,
            fight_id,
            fighter_b_id,
            fighter_a_id,
            fighter_b_outcome,
            fighter_b_method,
            fighter_b_round,
            fighter_b_sig_landed,
        ),
    )


def _insert_round_rows(cur, fight_id: str, fighter_id: str, rounds: int) -> None:
    for round_number in range(1, rounds + 1):
        cur.execute(
            """
            INSERT INTO fight_round_stats (
                fight_id,
                fighter_id,
                round,
                sig_strikes_landed,
                sig_strikes_attempted,
                total_strikes_landed,
                total_strikes_attempted
            )
            VALUES (%s, %s, %s, 10, 20, 15, 25)
            """,
            (fight_id, fighter_id, round_number),
        )
