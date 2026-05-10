"""Tests for UFC Fight Predictor ML feature construction."""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL is required for database-backed ML tests",
)

sys.path.insert(0, str(Path(__file__).parent))

from ml.db import pool
from ml.features import FEATURE_NAMES, build_features


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


def _delete_fixture(cur, prefix: str) -> None:
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
