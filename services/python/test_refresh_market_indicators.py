from datetime import UTC, date, datetime

import pytest

from ml.refresh_market_indicators import (
    refresh_indicator_rows,
    over_2_5_no_vig_market,
)


def _row(fight_id: str, fighter_id: str, status: str | None = "current") -> dict:
    return {
        "fight_id": fight_id,
        "event_id": "event-1",
        "event_date": date(2026, 6, 1),
        "weight_class": "lightweight",
        "fighter_id": fighter_id,
        "backfill_status": status,
    }


def test_over_2_5_no_vig_market_averages_complete_book_pairs():
    market = over_2_5_no_vig_market(
        [
            {
                "source_market_id": "m1",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome1",
                "implied_probability": 0.6,
            },
            {
                "source_market_id": "m1",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome2",
                "implied_probability": 0.5,
            },
            {
                "source_market_id": "m1",
                "sportsbook_slug": "book-b",
                "outcome_side": "outcome1",
                "implied_probability": 0.55,
            },
        ]
    )

    assert market == {"market_probability": 0.6 / 1.1, "pair_count": 1}


def test_refresh_indicator_rows_writes_idempotent_snapshot_payloads():
    written = []

    summary = refresh_indicator_rows(
        [_row("fight-1", "fighter-a"), _row("fight-1", "fighter-b")],
        computed_at=datetime(2026, 5, 16, tzinfo=UTC),
        indicator_fn=lambda _a, _b: {
            "target": "over_2_5",
            "label": "Over 2.5 rounds",
            "model_version": "locked_over_2_5_positive_log_c1_conf58",
            "model_probability": 0.64,
            "threshold": 0.58,
            "candidate": True,
            "value_status": "report_only",
            "value_status_reason": "forward tracking required",
            "training_sample_count": 123,
            "artifact_generated_at": "2026-05-16T00:00:00+00:00",
        },
        market_fn=lambda _fight_id: {"market_probability": 0.54, "pair_count": 3},
        write_fn=written.append,
    )

    assert summary["scanned"] == 1
    assert summary["written"] == 1
    assert summary["skipped"] == 0
    assert summary["missing_props"] == 0
    assert summary["errors"] == 0
    assert written[0]["fight_id"] == "fight-1"
    assert written[0]["target"] == "over_2_5"
    assert written[0]["model_probability"] == 0.64
    assert written[0]["market_probability"] == 0.54
    assert written[0]["edge_pct"] == pytest.approx(0.10)
    assert written[0]["value_status"] == "report_only"


def test_refresh_indicator_rows_skips_missing_backfill_and_counts_missing_props():
    written = []

    summary = refresh_indicator_rows(
        [
            _row("fight-1", "fighter-a"),
            _row("fight-1", "fighter-b", "none"),
            _row("fight-2", "fighter-c"),
            _row("fight-2", "fighter-d"),
        ],
        computed_at=datetime(2026, 5, 16, tzinfo=UTC),
        indicator_fn=lambda _a, _b: {
            "target": "over_2_5",
            "label": "Over 2.5 rounds",
            "model_version": "locked_over_2_5_positive_log_c1_conf58",
            "model_probability": 0.61,
            "threshold": 0.58,
            "candidate": True,
            "value_status": "report_only",
            "value_status_reason": "forward tracking required",
            "training_sample_count": 123,
        },
        market_fn=lambda _fight_id: None,
        write_fn=written.append,
    )

    assert summary["scanned"] == 2
    assert summary["written"] == 1
    assert summary["skipped"] == 1
    assert summary["missing_props"] == 1
    assert summary["skip_reasons"][0]["reason"] == "both fighters must have current backfill state"
    assert written[0]["value_status"] == "insufficient_coverage"
    assert written[0]["market_pair_count"] == 0
