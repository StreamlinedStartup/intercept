"""Tests for report-only market residual bucket analysis."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from ml.market_residual_analysis import (
    _bucket_report,
    _disagreement_bucket,
    _feature_availability_bucket,
    _unstable_reasons,
    render_markdown,
)


def _row(index: int, *, model_label: int, market_label: int, label: int) -> dict:
    return {
        "fight_id": f"fight-{index}",
        "event_id": f"event-{index // 10}",
        "event_date": "2026-01-01",
        "actual_label": label,
        "model": {
            "fighter_a_probability": 0.7 if model_label == 1 else 0.3,
            "predicted_label": model_label,
            "confidence": 0.7,
            "won": model_label == label,
            "decimal_odds": 2.0,
            "net_profit": 1.0 if model_label == label else -1.0,
        },
        "market": {
            "fighter_a_probability": 0.65 if market_label == 1 else 0.35,
            "predicted_label": market_label,
            "confidence": 0.65,
            "won": market_label == label,
            "decimal_odds": 2.0,
            "net_profit": 1.0 if market_label == label else -1.0,
        },
        "residuals": {
            "absolute_probability_delta": 0.05,
            "model_market_disagree": model_label != market_label,
        },
        "features": {"missing_rate": 0.0},
    }


def test_bucket_report_flags_unstable_and_computes_model_market_deltas() -> None:
    rows = [_row(index, model_label=1, market_label=0, label=1) for index in range(12)]

    bucket = _bucket_report("test", "small", rows)

    assert bucket["unstable"] is True
    assert "fewer_than_30_fights" in bucket["unstable_reasons"]
    assert bucket["model"]["metrics"]["accuracy"] == 1.0
    assert bucket["market"]["metrics"]["accuracy"] == 0.0
    assert bucket["deltas"]["accuracy_model_minus_market"] == 1.0
    assert bucket["deltas"]["roi_model_minus_market"] == pytest.approx(2.0)
    assert bucket["eligible_for_promotion_recommendations"] is False


def test_unstable_reasons_require_count_and_event_floor() -> None:
    assert _unstable_reasons(29, 5) == ["fewer_than_30_fights"]
    assert _unstable_reasons(30, 4) == ["fewer_than_5_events"]
    assert _unstable_reasons(30, 5) == []


def test_bucket_helpers_label_feature_availability_and_disagreement() -> None:
    row = _row(1, model_label=1, market_label=0, label=1)
    row["features"]["missing_rate"] = 0.2
    row["residuals"]["absolute_probability_delta"] = 0.25

    assert _feature_availability_bucket(row) == "partial"
    assert _disagreement_bucket(row) == "disagree_delta_20pp_plus"


def test_markdown_includes_policy_and_model_versions_contract() -> None:
    rows = [_row(index, model_label=1, market_label=1, label=1) for index in range(30)]
    report = {
        "generated_at": "2026-05-12T00:00:00+00:00",
        "value_status": "research_only",
        "writes_model_versions": False,
        "input_baseline": "data/experiments/market-residual-analysis-baseline.json",
        "coverage": {"scored_events": 5, "scored_fights": 30},
        "unstable_bucket_policy": {"min_fights": 30, "min_events": 5},
        "overall": _bucket_report("all", "all", rows),
        "dimensions": [{"name": "test", "label": "Test", "buckets": [_bucket_report("test", "all", rows)]}],
        "policy": "No model_versions writes or promotion recommendations.",
    }

    markdown = render_markdown(report)

    assert "# Market Residual Bucket Report" in markdown
    assert "Writes `model_versions`: `false`" in markdown
    assert "excluded from promotion recommendations" in markdown
