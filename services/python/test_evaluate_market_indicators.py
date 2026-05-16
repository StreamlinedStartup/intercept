import pytest

from ml.evaluate_market_indicators import (
    build_indicator_evaluation_report,
    elapsed_rounds,
    target_label,
)


def test_target_label_supports_method_and_round_total_targets():
    assert target_label({"target": "decision", "method": "Decision - Unanimous"}) == 1
    assert target_label({"target": "finish", "method": "KO/TKO", "round": 2, "time_seconds": 120}) == 1
    assert target_label({"target": "ko_tko", "method": "KO/TKO"}) == 1
    assert target_label({"target": "submission", "method": "Submission"}) == 1
    assert (
        target_label(
            {
                "target": "over_2_5",
                "method": "KO/TKO",
                "round": 3,
                "time_seconds": 180,
                "scheduled_rounds": 3,
            }
        )
        == 1
    )


def test_elapsed_rounds_uses_scheduled_rounds_for_decisions():
    assert elapsed_rounds(3, 0, 5, True) == 5.0
    assert elapsed_rounds(2, 150, 3, False) == pytest.approx(1.5)


def test_build_indicator_evaluation_report_summarizes_quality_without_activation():
    report = build_indicator_evaluation_report(
        [
            {
                "fight_id": "fight-1",
                "target": "over_2_5",
                "model_version": "v1",
                "model_probability": 0.64,
                "market_probability": 0.54,
                "edge_pct": 0.10,
                "candidate": True,
                "value_status": "report_only",
                "method": "Decision - Unanimous",
                "round": 3,
                "time_seconds": 0,
                "scheduled_rounds": 3,
            },
            {
                "fight_id": "fight-2",
                "target": "over_2_5",
                "model_version": "v1",
                "model_probability": 0.40,
                "market_probability": None,
                "edge_pct": None,
                "candidate": False,
                "value_status": "insufficient_coverage",
                "method": "KO/TKO",
                "round": 1,
                "time_seconds": 60,
                "scheduled_rounds": 3,
            },
        ]
    )

    assert report["report_only"] is True
    assert report["writes_model_versions"] is False
    assert report["activates_betting"] is False
    assert report["summary"] == {"snapshots": 2, "evaluated": 2, "skipped": 0, "targets": 1}
    assert report["targets"]["over_2_5"]["hit_rate"] == 1.0
    assert report["targets"]["over_2_5"]["candidate_hit_rate"] == 1.0
    assert report["targets"]["over_2_5"]["avg_edge_pct"] == 0.10
    assert report["targets"]["over_2_5"]["calibration_buckets"] == [
        {"bucket": "0.25-0.50", "count": 1, "avg_probability": 0.40, "actual_rate": 0.0},
        {"bucket": "0.50-0.75", "count": 1, "avg_probability": 0.64, "actual_rate": 1.0},
    ]
