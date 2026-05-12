"""Tests for the report-only market gate report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml.market_gate_report import _validation_gate, render_markdown


def test_validation_gate_blocks_insufficient_coverage() -> None:
    gate = _validation_gate(
        {"summary": {"scored_fights": 12, "scored_events": 3}},
        [
            {"name": "model_pick", "simulated_research_roi": {"roi_pct": 0.12}},
            {"name": "market_favorite", "simulated_research_roi": {"roi_pct": 0.02}},
        ],
    )

    assert gate["value_status"] == "insufficient_coverage"
    assert "need at least" in gate["value_status_reason"]


def test_validation_gate_keeps_research_only_without_market_lift() -> None:
    gate = _validation_gate(
        {"summary": {"scored_fights": 250, "scored_events": 40}},
        [
            {"name": "model_pick", "simulated_research_roi": {"roi_pct": 0.03}},
            {"name": "market_favorite", "simulated_research_roi": {"roi_pct": 0.02}},
        ],
    )

    assert gate["value_status"] == "research_only"
    assert "market-favorite baseline" in gate["value_status_reason"]


def test_market_gate_markdown_includes_policy() -> None:
    report = {
        "generated_at": "2026-05-12T00:00:00+00:00",
        "value_status": "insufficient_coverage",
        "value_status_reason": "Only 12 matched fights were scored.",
        "writes_model_versions": False,
        "coverage": {
            "scored_events": 3,
            "scored_fights": 12,
            "moneyline_rows_linked": 10,
            "moneyline_rows_imported": 20,
        },
        "timestamp_semantics": {"label": "Point-in-time report."},
        "strategies": [
            {
                "name": "market_favorite",
                "metrics": {
                    "count": 12,
                    "accuracy": 0.75,
                    "avg_confidence": 0.58,
                    "calibration_gap": 0.17,
                    "log_loss": 0.5,
                    "brier_score": 0.16,
                    "roc_auc": 0.8,
                },
                "simulated_research_roi": {"roi_pct": 0.02},
            }
        ],
    }

    markdown = render_markdown(report)

    assert "# Market Gate Report" in markdown
    assert "Value status: `insufficient_coverage`" in markdown
    assert "Writes `model_versions`: `false`" in markdown
    assert "not a promotion" in markdown
