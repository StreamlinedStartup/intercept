"""Tests for the config-driven market experiment harness."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from ml.experiment_harness import (
    _annotate_variant,
    _base_prediction_key,
    _calibrate_probability,
    _feature_count,
    _feature_names,
    _load_config,
    _materialize_predictions,
    _recommendation,
    _run_model_variant,
    _validate_config,
    render_markdown,
)


def _config() -> dict:
    return {
        "name": "test",
        "description": "test",
        "value_status": "research_only",
        "report_only": True,
        "writes_model_versions": False,
        "corpus": {
            "source": "matched_market_fights",
            "market_source": "fightodds_no_vig_consensus",
            "min_train_samples": 100,
            "max_events": None,
        },
        "split": {
            "policy": "chronological_walk_forward",
            "candidate_selection": "full_current_corpus",
            "locked_evaluation": "future_required",
        },
        "gate": {
            "baseline": "market_favorite",
            "min_roi_delta_vs_market": 0.02,
            "probability_quality": {
                "require_log_loss_not_worse": True,
                "require_brier_not_worse": True,
            },
        },
        "variants": [
            {"name": "market_favorite", "model": "market_favorite", "features": "none", "market_blend_weight": None}
        ],
        "outputs": {"json": "data/experiments/test.json", "markdown": "data/experiments/test.md"},
    }


def _variant(name: str, roi: float, log_loss: float, brier: float) -> dict:
    return {
        "name": name,
        "events_scored": 40,
        "metrics": {"count": 379, "accuracy": 0.6, "log_loss": log_loss, "brier_score": brier},
        "simulated_research_roi": {"roi_pct": roi},
    }


def test_load_config_accepts_checked_in_example() -> None:
    config = _load_config(Path("configs/experiments/market-grid.example.json"))

    assert config["value_status"] == "research_only"
    assert config["writes_model_versions"] is False
    assert len(config["variants"]) >= 4


def test_load_config_accepts_real_axes_smoke_example() -> None:
    config = _load_config(Path("configs/experiments/market-grid-real-axes-smoke.json"))

    variants = {variant["name"]: variant for variant in config["variants"]}
    assert config["value_status"] == "research_only"
    assert config["writes_model_versions"] is False
    assert variants["xgb_shallow"]["model_params"]["max_depth"] == 2
    assert variants["xgb_no_recent_form"]["feature_subset"]["mode"] == "exclude"
    assert variants["xgb_temperature_150"]["calibration"]["temperature"] == 1.5


def test_validate_config_rejects_active_model_writes() -> None:
    config = _config()
    config["writes_model_versions"] = True

    with pytest.raises(ValueError, match="writes_model_versions=false"):
        _validate_config(config)


def test_validate_config_rejects_unsupported_model_params() -> None:
    config = _config()
    config["variants"].append(
        {
            "name": "bad",
            "model": "xgboost",
            "features": "production",
            "model_params": {"unsupported": 1},
        }
    )

    with pytest.raises(ValueError, match="unsupported model_params"):
        _validate_config(config)


def test_feature_subset_resolves_named_groups() -> None:
    variant = {
        "name": "xgb_no_recent_form",
        "model": "xgboost",
        "features": "production",
        "feature_subset": {"mode": "exclude", "names": ["recent_form"]},
    }

    names = _feature_names(variant)

    assert "wins_last_3_diff" not in names
    assert "slpm_diff" in names
    assert _feature_count(variant) == len(names)


def test_feature_count_tracks_availability_alignment() -> None:
    assert _feature_count("none") == 0
    assert _feature_count("production_plus_availability") == _feature_count("production") + 4


def test_base_prediction_key_ignores_blend_and_calibration() -> None:
    base = {"name": "a", "model": "xgboost", "features": "production", "market_blend_weight": 0.1}
    same_base = {
        "name": "b",
        "model": "xgboost",
        "features": "production",
        "market_blend_weight": 0.9,
        "calibration": {"method": "temperature", "temperature": 1.5},
    }
    different = {
        "name": "c",
        "model": "xgboost",
        "features": "production",
        "model_params": {"max_depth": 2},
    }

    assert _base_prediction_key(base, 100) == _base_prediction_key(same_base, 100)
    assert _base_prediction_key(base, 100) != _base_prediction_key(different, 100)


def test_calibration_is_deterministic_and_bounded() -> None:
    assert _calibrate_probability(0.8, {"method": "none"}) == pytest.approx(0.8)
    assert _calibrate_probability(0.8, {"method": "temperature", "temperature": 2.0}) < 0.8
    assert 0 < _calibrate_probability(1.0, {"method": "temperature", "temperature": 2.0}) < 1


def test_materialize_predictions_calibrates_before_blending() -> None:
    sample = {
        "fight_id": "fight-1",
        "event_id": "event-1",
        "event_date": __import__("datetime").date(2026, 1, 1),
        "fighter_a_id": "a",
        "fighter_b_id": "b",
        "label": 1,
    }
    markets = {"fight-1": {"a": {"market_prob": 0.6, "decimal_odds": 2.0}, "b": {"market_prob": 0.4, "decimal_odds": 2.0}}}

    predictions = _materialize_predictions(
        [{"sample": sample, "model_probability": 0.8}],
        markets,
        {"method": "temperature", "temperature": 2.0},
        0.5,
    )

    calibrated = _calibrate_probability(0.8, {"method": "temperature", "temperature": 2.0})
    assert predictions[0]["fighter_a_probability"] == pytest.approx((calibrated + 0.6) / 2)


def test_run_model_variant_reuses_base_prediction_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def fake_score(*args: object, **kwargs: object) -> list[dict]:
        nonlocal calls
        calls += 1
        return []

    monkeypatch.setattr("ml.experiment_harness._score_base_walk_forward", fake_score)
    cache: dict[tuple, list[dict]] = {}
    first = {"name": "a", "model": "xgboost", "features": "production", "market_blend_weight": 0.1}
    second = {"name": "b", "model": "xgboost", "features": "production", "market_blend_weight": 0.9}

    _run_model_variant(first, [], [], {}, 100, cache)
    _run_model_variant(second, [], [], {}, 100, cache)

    assert calls == 1


def test_gate_annotation_requires_roi_and_probability_quality() -> None:
    market = _variant("market_favorite", roi=0.10, log_loss=0.50, brier=0.18)
    candidate = _variant("candidate", roi=0.13, log_loss=0.55, brier=0.17)

    _annotate_variant(candidate, market, _config()["gate"])

    assert candidate["roi_delta_vs_market"] == pytest.approx(0.03)
    assert candidate["clears_market_gate"] is False
    assert candidate["rejection_reasons"] == ["log_loss_worse_than_market"]


def test_recommendation_requires_locked_followup_for_passing_candidate() -> None:
    candidate = _variant("candidate", roi=0.13, log_loss=0.45, brier=0.17)
    market = _variant("market_favorite", roi=0.10, log_loss=0.50, brier=0.18)
    _annotate_variant(candidate, market, _config()["gate"])

    recommendation = _recommendation([candidate, market])

    assert recommendation["status"] == "candidate_for_locked_evaluation"
    assert "locked future slice" in recommendation["reason"]


def test_markdown_includes_research_only_contract() -> None:
    report = {
        "generated_at": "2026-05-12T00:00:00+00:00",
        "config_path": "configs/experiments/market-grid.example.json",
        "value_status": "research_only",
        "writes_model_versions": False,
        "coverage": {"model_eligible_events": 1, "model_eligible_fights": 1},
        "ranking": [
            {
                "rank": 1,
                "name": "candidate",
                "roi_delta_vs_market": 0.01,
                "log_loss_delta_vs_market": 0.0,
                "brier_delta_vs_market": 0.0,
                "clears_gate": False,
                "rejection_reasons": ["roi_delta_below_market_gate"],
            }
        ],
        "variants": [
            {
                "name": "candidate",
                "params": {"model": "xgboost", "features": "production", "market_blend_weight": None},
                "metrics": {"count": 1, "accuracy": 1.0, "log_loss": 0.1, "brier_score": 0.1},
                "simulated_research_roi": {"roi_pct": 0.1},
            }
        ],
        "recommendation": {"status": "research_only", "reason": "test"},
        "policy": "report-only policy",
    }

    markdown = render_markdown(report)

    assert "Writes `model_versions`: `false`" in markdown
    assert "report-only policy" in markdown
