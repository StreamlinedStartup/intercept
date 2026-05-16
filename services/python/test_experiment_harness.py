"""Tests for the config-driven market experiment harness."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from ml.experiment_harness import (
    MARKET_CONTEXT_FEATURE_NAMES,
    _annotate_variant,
    _apply_holdout_policy,
    _apply_selection_policy,
    _attach_market_context,
    _base_prediction_key,
    _calibrate_probability,
    _feature_count,
    _feature_names,
    _holdout_policy,
    _holdout_summary,
    _load_config,
    _materialize_predictions,
    _method_probabilities_from_raw_metadata,
    _novig_distance_probabilities,
    _novig_over_under_probabilities,
    _prop_market_consensus_from_rows,
    _prop_market_probability,
    _round_total_labels,
    _recommendation,
    _run_model_variant,
    _signal_diagnostics,
    _target,
    _target_label,
    _target_prediction,
    _target_roi,
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


def _variant(name: str, roi: float, log_loss: float, brier: float, target: str = "winner") -> dict:
    return {
        "name": name,
        "params": {"target": target},
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


def test_load_config_accepts_market_opportunity_configs() -> None:
    smoke = _load_config(Path("configs/experiments/market-opportunity-smoke.json"))
    matrix = _load_config(Path("configs/experiments/market-opportunity-matrix-v1.json"))
    locked = _load_config(Path("configs/experiments/prop-signal-locked-validation-v1.json"))
    method_round = _load_config(Path("configs/experiments/method-round-prop-targets-v1.json"))

    smoke_variants = {variant["name"]: variant for variant in smoke["variants"]}
    matrix_variants = {variant["name"]: variant for variant in matrix["variants"]}
    locked_variants = {variant["name"]: variant for variant in locked["variants"]}
    method_round_variants = {variant["name"]: variant for variant in method_round["variants"]}
    assert smoke_variants["decision_edge_smoke"]["target"] == "decision"
    assert smoke_variants["finish_edge_smoke"]["selection_policy"]["type"] == "finish_edge"
    assert matrix_variants["winner_overpriced_favorite_log_c1_edge05"]["selection_policy"]["type"] == "overpriced_favorite"
    assert matrix_variants["winner_underdog_blend40_edge04"]["market_blend_weight"] == 0.4
    assert locked["corpus"]["holdout"] == {"type": "last_n_events", "event_count": 20}
    assert locked_variants["locked_decision_market_strength_conf62"]["target"] == "decision"
    assert method_round_variants["ko_tko_positive_log_c1_conf32"]["target"] == "ko_tko"
    assert method_round_variants["over_2_5_positive_log_c1_conf58"]["selection_policy"]["type"] == "positive_target_edge"


def test_validate_config_rejects_active_model_writes() -> None:
    config = _config()
    config["writes_model_versions"] = True

    with pytest.raises(ValueError, match="writes_model_versions=false"):
        _validate_config(config)


def test_variant_target_defaults_to_winner() -> None:
    assert _target({"name": "candidate", "model": "xgboost", "features": "production"}) == "winner"


def test_validate_config_accepts_decision_and_finish_targets() -> None:
    config = _config()
    config["variants"].extend(
        [
            {"name": "decision_candidate", "model": "xgboost", "target": "decision", "features": "production"},
            {"name": "finish_candidate", "model": "logistic_regression", "target": "finish", "features": "production"},
        ]
    )

    _validate_config(config)


def test_validate_config_rejects_unknown_target() -> None:
    config = _config()
    config["variants"].append(
        {"name": "bad_target", "model": "xgboost", "target": "doctor_stoppage", "features": "production"}
    )

    with pytest.raises(ValueError, match="unsupported target"):
        _validate_config(config)


def test_validate_config_rejects_non_winner_market_favorite_target() -> None:
    config = _config()
    config["variants"][0]["target"] = "decision"

    with pytest.raises(ValueError, match="market_favorite baseline only supports target='winner'"):
        _validate_config(config)


def test_validate_config_rejects_market_blend_for_non_winner_target() -> None:
    config = _config()
    config["variants"].append(
        {
            "name": "decision_blend",
            "model": "xgboost",
            "target": "decision",
            "features": "production",
            "market_blend_weight": 0.5,
        }
    )

    with pytest.raises(ValueError, match="market_blend_weight requires target='winner'"):
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
    assert _feature_count("production_plus_opponent_adjusted_recent_performance") == _feature_count("production") + 4
    assert _feature_count("production_plus_style_matchup_pressure") == _feature_count("production") + 3
    assert _feature_count("production_plus_market_context") == _feature_count("production") + 4
    assert _feature_count("production_plus_all_research_market_context") == _feature_count("production") + 15


def test_market_context_features_are_declared_and_point_in_time_attached() -> None:
    variant = {"name": "market_context", "model": "xgboost", "features": "production_plus_market_context"}
    sample = {
        "fight_id": "fight-1",
        "fighter_a_id": "a",
        "fighter_b_id": "b",
        "features": __import__("numpy").array([1.0]),
    }
    markets = {"fight-1": {"a": {"market_prob": 0.62}, "b": {"market_prob": 0.38}}}

    enriched = _attach_market_context([sample], markets)

    assert _feature_names(variant)[-4:] == MARKET_CONTEXT_FEATURE_NAMES
    assert enriched[0]["market_context_features"].tolist() == pytest.approx([0.62, 0.38, 0.24, 0.38])


def test_holdout_policy_keeps_last_n_chronological_events() -> None:
    from datetime import date

    samples = [
        {"event_id": "e1", "event_date": date(2026, 1, 1), "fight_id": "f1"},
        {"event_id": "e2", "event_date": date(2026, 1, 2), "fight_id": "f2"},
        {"event_id": "e3", "event_date": date(2026, 1, 3), "fight_id": "f3"},
        {"event_id": "e4", "event_date": date(2026, 1, 4), "fight_id": "f4"},
    ]

    holdout = _apply_holdout_policy(samples, {"type": "last_n_events", "event_count": 2})

    assert [sample["event_id"] for sample in holdout] == ["e3", "e4"]
    assert _holdout_summary({"type": "last_n_events", "event_count": 2}, holdout) == {
        "type": "last_n_events",
        "event_count": 2,
        "events": 2,
        "fights": 2,
        "start_date": "2026-01-03",
        "end_date": "2026-01-04",
    }


def test_holdout_policy_keeps_events_after_date() -> None:
    from datetime import date

    samples = [
        {"event_id": "e1", "event_date": date(2024, 3, 9), "fight_id": "f1"},
        {"event_id": "e2", "event_date": date(2024, 3, 10), "fight_id": "f2"},
        {"event_id": "e3", "event_date": date(2026, 1, 3), "fight_id": "f3"},
    ]

    holdout = _apply_holdout_policy(samples, {"type": "after_date", "after_date": "2024-03-09"})

    assert [sample["event_id"] for sample in holdout] == ["e2", "e3"]
    assert _holdout_summary({"type": "after_date", "after_date": "2024-03-09"}, holdout) == {
        "type": "after_date",
        "after_date": "2024-03-09",
        "events": 2,
        "fights": 2,
        "start_date": "2024-03-10",
        "end_date": "2026-01-03",
    }


def test_holdout_policy_rejects_invalid_policy() -> None:
    with pytest.raises(ValueError, match="unsupported holdout policy"):
        _holdout_policy({"type": "random", "event_count": 2})

    with pytest.raises(ValueError, match="event_count >= 1"):
        _holdout_policy({"type": "last_n_events", "event_count": 0})

    with pytest.raises(ValueError, match="after_date requires after_date"):
        _holdout_policy({"type": "after_date"})


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


def test_base_prediction_key_includes_target() -> None:
    winner = {"name": "a", "model": "xgboost", "features": "production", "target": "winner"}
    decision = {"name": "b", "model": "xgboost", "features": "production", "target": "decision"}

    assert _base_prediction_key(winner, 100) != _base_prediction_key(decision, 100)


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
        {},
        {"method": "temperature", "temperature": 2.0},
        0.5,
    )

    calibrated = _calibrate_probability(0.8, {"method": "temperature", "temperature": 2.0})
    assert predictions[0]["fighter_a_probability"] == pytest.approx((calibrated + 0.6) / 2)


def test_target_label_reads_winner_decision_and_finish_labels() -> None:
    sample = {"label": 1, "target_labels": {"decision": 0, "finish": 1, "ko_tko": 1, "over_2_5": 0}}

    assert _target_label(sample, "winner") == 1
    assert _target_label(sample, "decision") == 0
    assert _target_label(sample, "finish") == 1
    assert _target_label(sample, "ko_tko") == 1
    assert _target_label(sample, "over_2_5") == 0
    assert _target_label({"label": 0}, "decision") is None


def test_non_winner_target_prediction_uses_target_label_without_market_roi() -> None:
    sample = {
        "fight_id": "fight-1",
        "event_id": "event-1",
        "event_date": __import__("datetime").date(2026, 1, 1),
        "label": 0,
        "target_labels": {"decision": 1, "finish": 0},
    }

    prediction = _target_prediction(sample, {}, {}, 0.7, None, "decision")

    assert prediction["target"] == "decision"
    assert prediction["actual_label"] == 1
    assert prediction["predicted_label"] == 1
    assert prediction["won"] is True
    assert prediction["market_probability"] is None
    assert _target_roi("decision", [prediction])["status"] == "decision_market_odds_unavailable"


def test_non_winner_target_prediction_uses_prop_market_roi() -> None:
    sample = {
        "fight_id": "fight-1",
        "event_id": "event-1",
        "event_date": __import__("datetime").date(2026, 1, 1),
        "label": 0,
        "target_labels": {"decision": 1, "finish": 0},
    }
    prop_markets = {"fight-1": {"decision": {"market_prob": 0.55, "pair_count": 2}}}

    prediction = _target_prediction(sample, {}, prop_markets, 0.7, None, "decision")
    roi = _target_roi("decision", [prediction])

    assert prediction["market_probability"] == pytest.approx(0.55)
    assert prediction["market_predicted_label"] == 1
    assert prediction["picked_market_probability"] == pytest.approx(0.55)
    assert prediction["picked_model_market_edge"] == pytest.approx(0.15)
    assert prediction["decimal_odds"] == pytest.approx(1 / 0.55)
    assert prediction["net_profit"] == pytest.approx((1 / 0.55) - 1)
    assert roi["status"] == "simulated_research_only"
    assert roi["entries"] == 1
    assert roi["wins"] == 1


def test_finish_target_prediction_uses_complement_prop_market_roi() -> None:
    sample = {
        "fight_id": "fight-1",
        "event_id": "event-1",
        "event_date": __import__("datetime").date(2026, 1, 1),
        "label": 0,
        "target_labels": {"decision": 1, "finish": 0},
    }
    prop_markets = {"fight-1": {"finish": {"market_prob": 0.45, "pair_count": 2}}}

    prediction = _target_prediction(sample, {}, prop_markets, 0.3, None, "finish")

    assert prediction["predicted_label"] == 0
    assert prediction["market_predicted_label"] == 0
    assert prediction["picked_market_probability"] == pytest.approx(0.55)
    assert prediction["picked_model_market_edge"] == pytest.approx(0.15)
    assert _target_roi("finish", [prediction])["status"] == "simulated_research_only"


def test_non_winner_target_prediction_rejects_market_blend() -> None:
    sample = {
        "fight_id": "fight-1",
        "event_id": "event-1",
        "event_date": __import__("datetime").date(2026, 1, 1),
        "target_labels": {"finish": 1},
    }

    with pytest.raises(ValueError, match="market_blend_weight requires target='winner'"):
        _target_prediction(sample, {}, {}, 0.7, 0.5, "finish")


def test_novig_distance_probabilities_require_paired_outcomes() -> None:
    assert _novig_distance_probabilities({"outcome1": 0.6}) is None
    probabilities = _novig_distance_probabilities({"outcome1": 0.6, "outcome2": 0.5})

    assert probabilities is not None
    assert probabilities["decision"] == pytest.approx(0.6 / 1.1)
    assert probabilities["finish"] == pytest.approx(0.5 / 1.1)


def test_novig_over_under_probabilities_map_offer_type_to_target() -> None:
    assert _novig_over_under_probabilities("OVERUNDER_2.5", {"outcome1": 0.6}) is None
    probabilities = _novig_over_under_probabilities("OVERUNDER_2.5", {"outcome1": 0.6, "outcome2": 0.5})

    assert probabilities is not None
    assert probabilities["over_2_5"] == pytest.approx(0.6 / 1.1)


def test_method_probabilities_normalize_fight_level_method_odds() -> None:
    probabilities = _method_probabilities_from_raw_metadata(
        {
            "propFight": {
                "fighter1KoOdds": 100,
                "fighter2KoOdds": 300,
                "fighter1SubOdds": 400,
                "fighter2SubOdds": 900,
                "fighter1DecOdds": 200,
                "fighter2DecOdds": 600,
            }
        }
    )

    assert probabilities is not None
    assert probabilities["ko_tko"] > probabilities["submission"]
    assert probabilities["ko_tko"] + probabilities["submission"] < 1


def test_round_total_labels_use_elapsed_rounds() -> None:
    assert _round_total_labels(None) == {}
    assert _round_total_labels(2.6)["over_2_5"] == 1
    assert _round_total_labels(2.4)["over_2_5"] == 0


def test_prop_market_consensus_maps_distance_rows_to_targets() -> None:
    consensus = _prop_market_consensus_from_rows(
        [
            {
                "fight_id": "fight-1",
                "source_market_id": "market-1",
                "source_offer_type_id": "DISTANCE",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome1",
                "implied_probability": 0.60,
            },
            {
                "fight_id": "fight-1",
                "source_market_id": "market-1",
                "source_offer_type_id": "DISTANCE",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome2",
                "implied_probability": 0.50,
            },
            {
                "fight_id": "fight-1",
                "source_market_id": "market-1",
                "source_offer_type_id": "DISTANCE",
                "sportsbook_slug": "book-b",
                "outcome_side": "outcome1",
                "implied_probability": 0.55,
            },
            {
                "fight_id": "fight-1",
                "source_market_id": "market-1",
                "source_offer_type_id": "DISTANCE",
                "sportsbook_slug": "book-b",
                "outcome_side": "outcome2",
                "implied_probability": 0.55,
            },
            {
                "fight_id": "fight-2",
                "source_market_id": "market-2",
                "source_offer_type_id": "DISTANCE",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome1",
                "implied_probability": 0.60,
            },
        ]
    )

    expected_decision = ((0.60 / 1.10) + (0.55 / 1.10)) / 2
    assert consensus["fight-1"]["decision"]["market_prob"] == pytest.approx(expected_decision)
    assert consensus["fight-1"]["finish"]["market_prob"] == pytest.approx(1 - expected_decision)
    assert consensus["fight-1"]["decision"]["pair_count"] == 2
    assert "fight-2" not in consensus
    assert _prop_market_probability(consensus, "fight-1", "decision") == pytest.approx(expected_decision)
    assert _prop_market_probability(consensus, "fight-1", "finish") == pytest.approx(1 - expected_decision)
    assert _prop_market_probability(consensus, "fight-1", "winner") is None
    assert _prop_market_probability(consensus, "missing", "decision") is None


def test_prop_market_consensus_maps_over_under_rows_to_targets() -> None:
    consensus = _prop_market_consensus_from_rows(
        [
            {
                "fight_id": "fight-1",
                "source_market_id": "market-ou",
                "source_offer_type_id": "OVERUNDER_2.5",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome1",
                "implied_probability": 0.60,
            },
            {
                "fight_id": "fight-1",
                "source_market_id": "market-ou",
                "source_offer_type_id": "OVERUNDER_2.5",
                "sportsbook_slug": "book-a",
                "outcome_side": "outcome2",
                "implied_probability": 0.50,
            },
        ]
    )

    assert consensus["fight-1"]["over_2_5"]["market_prob"] == pytest.approx(0.6 / 1.1)


def test_opportunity_selection_policies_pick_expected_rows() -> None:
    predictions = [
        {
            "fight_id": "overpriced-favorite",
            "target": "winner",
            "market_predicted_label": 1,
            "predicted_label": 0,
            "market_probability": 0.75,
            "fighter_a_probability": 0.55,
            "picked_model_market_edge": 0.10,
            "confidence": 0.45,
        },
        {
            "fight_id": "undervalued-underdog",
            "target": "winner",
            "market_predicted_label": 1,
            "predicted_label": 0,
            "market_probability": 0.70,
            "fighter_a_probability": 0.40,
            "picked_model_market_edge": 0.20,
            "confidence": 0.60,
        },
        {
            "fight_id": "decision-edge",
            "target": "decision",
            "predicted_label": 1,
            "picked_model_probability": 0.68,
            "confidence": 0.68,
            "market_predicted_label": None,
        },
        {
            "fight_id": "finish-edge",
            "target": "finish",
            "predicted_label": 1,
            "picked_model_probability": 0.66,
            "confidence": 0.66,
            "market_predicted_label": None,
        },
        {
            "fight_id": "ko-edge",
            "target": "ko_tko",
            "predicted_label": 1,
            "picked_model_probability": 0.64,
            "confidence": 0.64,
            "market_predicted_label": None,
        },
        {
            "fight_id": "pass",
            "target": "winner",
            "market_predicted_label": 1,
            "predicted_label": 1,
            "market_probability": 0.53,
            "fighter_a_probability": 0.52,
            "picked_model_market_edge": -0.01,
            "confidence": 0.52,
        },
    ]

    assert [
        row["fight_id"]
        for row in _apply_selection_policy(predictions, {"type": "overpriced_favorite", "threshold": 0.15})
    ] == ["overpriced-favorite", "undervalued-underdog"]
    assert [
        row["fight_id"]
        for row in _apply_selection_policy(predictions, {"type": "undervalued_underdog", "threshold": 0.15})
    ] == ["undervalued-underdog"]
    assert [
        row["fight_id"]
        for row in _apply_selection_policy(predictions, {"type": "decision_edge", "threshold": 0.65})
    ] == ["decision-edge"]
    assert [
        row["fight_id"]
        for row in _apply_selection_policy(predictions, {"type": "finish_edge", "threshold": 0.65})
    ] == ["finish-edge"]
    assert [
        row["fight_id"]
        for row in _apply_selection_policy(predictions, {"type": "positive_target_edge", "threshold": 0.63})
    ] == ["decision-edge", "finish-edge", "ko-edge"]
    assert [row["fight_id"] for row in _apply_selection_policy(predictions, {"type": "abstain", "threshold": 0.55})] == [
        "overpriced-favorite",
        "pass",
    ]


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

    _run_model_variant(first, [], [], {}, {}, 100, cache)
    _run_model_variant(second, [], [], {}, {}, 100, cache)

    assert calls == 1


def test_gate_annotation_requires_roi_and_probability_quality() -> None:
    market = _variant("market_favorite", roi=0.10, log_loss=0.50, brier=0.18)
    candidate = _variant("candidate", roi=0.13, log_loss=0.55, brier=0.17)

    _annotate_variant(candidate, market, _config()["gate"])

    assert candidate["roi_delta_vs_market"] == pytest.approx(0.03)
    assert candidate["clears_market_gate"] is False


def test_gate_annotation_compares_non_winner_to_same_target_prop_baseline() -> None:
    market = _variant("decision_market_baseline", roi=-0.02, log_loss=0.70, brier=0.24, target="decision")
    candidate = _variant("decision_candidate", roi=0.03, log_loss=0.69, brier=0.23, target="decision")

    _annotate_variant(candidate, market, _config()["gate"])

    assert candidate["roi_delta_vs_market"] == pytest.approx(0.05)
    assert candidate["log_loss_delta_vs_market"] == pytest.approx(-0.01)
    assert "market_baseline_unavailable_for_target" not in candidate["rejection_reasons"]
    assert candidate["rejection_reasons"] == []
    assert candidate["clears_market_gate"] is True


def test_recommendation_requires_locked_followup_for_passing_candidate() -> None:
    candidate = _variant("candidate", roi=0.13, log_loss=0.45, brier=0.17)
    market = _variant("market_favorite", roi=0.10, log_loss=0.50, brier=0.18)
    _annotate_variant(candidate, market, _config()["gate"])

    recommendation = _recommendation([candidate, market])

    assert recommendation["status"] == "candidate_for_locked_evaluation"
    assert "locked future slice" in recommendation["reason"]


def test_signal_diagnostics_surface_market_strength_reads() -> None:
    market = _variant("market_favorite", roi=0.10, log_loss=0.50, brier=0.18)
    candidate = _variant("winner_underdog", roi=-0.20, log_loss=0.80, brier=0.30)
    candidate["params"]["selection_policy"] = {"type": "undervalued_underdog"}
    candidate["gate_baseline"] = _variant("winner_underdog_market_baseline", roi=0.24, log_loss=0.52, brier=0.19)

    diagnostics = _signal_diagnostics([market, candidate], market)

    assert diagnostics[0]["variant"] == "winner_underdog"
    assert diagnostics[0]["indicator"] == "market_too_strong_against_model_underdog"
    assert diagnostics[0]["selected_market_roi_delta_vs_full_market"] == pytest.approx(0.14)


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
                "params": {
                    "model": "xgboost",
                    "target": "winner",
                    "features": "production",
                    "market_blend_weight": None,
                    "selection_policy": {"type": "all"},
                },
                "metrics": {"count": 1, "accuracy": 1.0, "log_loss": 0.1, "brier_score": 0.1},
                "simulated_research_roi": {"roi_pct": 0.1},
            }
        ],
        "signal_diagnostics": [
            {
                "variant": "candidate",
                "indicator": "market_too_strong_against_model_underdog",
                "model_roi_pct": -0.2,
                "selected_market_roi_pct": 0.24,
                "selected_market_roi_delta_vs_full_market": 0.14,
                "selected_market_entries": 10,
                "read": "Model disagreement is currently more useful as a market-strength warning than as a bet-against-market signal.",
            }
        ],
        "recommendation": {"status": "research_only", "reason": "test"},
        "policy": "report-only policy",
    }

    markdown = render_markdown(report)

    assert "Writes `model_versions`: `false`" in markdown
    assert "## Signal Diagnostics" in markdown
    assert "market_too_strong_against_model_underdog" in markdown
    assert "report-only policy" in markdown
