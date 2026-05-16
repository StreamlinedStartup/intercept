"""Tests for high-loss market residual cluster analysis."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml.market_residual_clusters import (
    _actionable_feature_gaps,
    _classification,
    _feature_summary,
    _is_high_loss_cluster,
    render_markdown,
)
from ml.market_residual_analysis import _bucket_report
from test_market_residual_analysis import _row


def test_high_loss_cluster_detects_bad_roi_delta() -> None:
    rows = [_row(index, model_label=1, market_label=0, label=0) for index in range(30)]
    cluster = {
        "bucket_report": _bucket_report("test", "model_on_market_underdog", rows),
        "failure_profile": {"high_conf_wrong_rate": 1.0},
    }

    assert _is_high_loss_cluster(cluster) is True


def test_actionable_feature_gaps_compare_cluster_to_corpus() -> None:
    corpus = {
        "average_missing_rate": 0.05,
        "availability_rates": {
            "has_recent_form": 0.95,
            "has_physical_profile": 0.9,
            "has_weight_context": 0.9,
            "has_common_opponents": 0.5,
        },
    }
    cluster = {
        "average_missing_rate": 0.15,
        "availability_rates": {
            "has_recent_form": 0.7,
            "has_physical_profile": 0.9,
            "has_weight_context": 0.85,
            "has_common_opponents": 0.45,
        },
    }

    assert _actionable_feature_gaps(cluster, corpus) == [
        "higher_feature_missingness",
        "lower_has_recent_form",
    ]


def test_classification_separates_actionable_market_and_unstable() -> None:
    stable_bucket = {"unstable": False, "bucket": "model_on_market_underdog"}
    unstable_bucket = {"unstable": True, "bucket": "heavyweight"}

    assert _classification(stable_bucket, ["lower_has_recent_form"]) == "actionable_pre_fight_feature_gap"
    assert _classification(stable_bucket, []) == "market_prior_gap"
    assert _classification(unstable_bucket, ["lower_has_recent_form"]) == "unstable_or_noise"


def test_feature_summary_and_markdown_include_contract() -> None:
    rows = [_row(index, model_label=1, market_label=0, label=0) for index in range(30)]
    for row in rows:
        row["features"] = {
            "missing_rate": 0.1,
            "missing_count": 4,
            "has_recent_form": False,
            "has_physical_profile": True,
            "has_weight_context": True,
            "has_common_opponents": False,
        }
    feature_summary = _feature_summary(rows)
    bucket = _bucket_report("test", "model_on_market_underdog", rows)
    report = {
        "generated_at": "2026-05-12T00:00:00+00:00",
        "value_status": "research_only",
        "writes_model_versions": False,
        "input_report": "data/experiments/market-residual-buckets.json",
        "coverage": {"model_eligible_events": 5, "model_eligible_fights": 30},
        "clusters": [
            {
                "dimension": "test",
                "bucket": "model_on_market_underdog",
                "bucket_report": bucket,
                "failure_profile": {"high_conf_wrong_rate": 1.0},
                "classification": "market_prior_gap",
                "actionable_feature_gaps": [],
            }
        ],
        "corpus_feature_summary": feature_summary,
        "recommendation_policy": "Stable actionable clusters only.",
        "policy": "No model_versions writes.",
    }

    markdown = render_markdown(report)

    assert feature_summary["availability_rates"]["has_recent_form"] == 0.0
    assert "Writes `model_versions`: `false`" in markdown
    assert "Stable actionable clusters only." in markdown
