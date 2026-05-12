"""Tests for report-only simple model baselines."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL is required for database-backed baseline tests",
)

sys.path.insert(0, str(Path(__file__).parent))

from ml.baselines import render_markdown, run_simple_baselines


def test_simple_baselines_report_is_research_only(tmp_path: Path) -> None:
    report = run_simple_baselines(
        max_events=1,
        output_path=tmp_path / "baselines.json",
        markdown_path=tmp_path / "baselines.md",
    )

    assert report["report_only"] is True
    assert report["writes_model_versions"] is False
    assert report["value_status"] == "research_only"
    assert {baseline["name"] for baseline in report["baselines"]} == {
        "ufc_experience",
        "recent_form_wins_last_3",
        "younger_fighter",
        "market_favorite",
    }


def test_simple_baselines_markdown_includes_simulated_roi(tmp_path: Path) -> None:
    report = run_simple_baselines(
        max_events=1,
        output_path=tmp_path / "baselines.json",
        markdown_path=tmp_path / "baselines.md",
    )
    markdown = render_markdown(report)

    assert "# Simple Leak-Free Baselines" in markdown
    assert "Sim ROI" in markdown
    assert "do not train" in markdown
