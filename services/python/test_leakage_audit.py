"""Tests for the report-only model leakage audit."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml.leakage_audit import render_markdown, run_leakage_audit


def test_source_leakage_audit_passes_without_database() -> None:
    report = run_leakage_audit(include_db=False)

    assert report["status"] == "pass"
    assert report["report_only"] is True
    assert report["writes_model_versions"] is False
    assert report["summary"]["failed"] == 0
    assert report["summary"]["checks"] >= 10


def test_leakage_audit_markdown_renders_policy() -> None:
    report = run_leakage_audit(include_db=False)
    markdown = render_markdown(report)

    assert "# Model Leakage Audit" in markdown
    assert "Writes `model_versions`: `false`" in markdown
    assert "It does not train a model" in markdown
