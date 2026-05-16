# Market Experiment Harness

- Generated: `2026-05-16T02:34:35.287572+00:00`
- Config: `configs/experiments/prop-signal-locked-validation-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 20
- Model-eligible fights: 206

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | locked_finish_proxy_conf62 | -7.6% | 0.1137 | 0.0429 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | locked_decision_market_strength_conf62 | -17.6% | 0.1093 | 0.0475 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 3 | locked_market_favorite_holds_edge05 | -24.7% | 0.1021 | 0.0432 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 4 | locked_market_strength_underdog_log_c1_edge05 | -103.6% | 0.2229 | 0.0986 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 5 | locked_market_strength_underdog_blend40_edge04 | -170.7% | 0.2401 | 0.1179 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 6 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | winner | market_favorite | none |  | 206 | 75.2% | 0.5627 | 0.1900 | 10.5% |
| locked_market_strength_underdog_blend40_edge04 | winner | logistic_regression | production_plus_all_research_market_context | 0.4 | 3 | 0.0% | 0.7975 | 0.3018 | -100.0% |
| locked_market_strength_underdog_log_c1_edge05 | winner | logistic_regression | production_plus_all_research_market_context |  | 20 | 15.0% | 0.8521 | 0.3161 | -58.5% |
| locked_market_favorite_holds_edge05 | winner | logistic_regression | production_plus_all_research_market_context |  | 84 | 65.5% | 0.6147 | 0.2107 | -7.5% |
| locked_decision_market_strength_conf62 | decision | logistic_regression | production_plus_all_research |  | 26 | 57.7% | 0.7083 | 0.2530 | -6.9% |
| locked_finish_proxy_conf62 | finish | logistic_regression | production_plus_all_research |  | 53 | 50.9% | 0.7761 | 0.2800 | -26.0% |

## Signal Diagnostics

| Variant | Indicator | Model ROI | Selected market ROI | Market ROI delta | Entries | Read |
|---|---|---:|---:|---:|---:|---|
| locked_market_strength_underdog_blend40_edge04 | market_too_strong_against_model_underdog | -100.0% | 70.7% | +60.2% | 3 | Model disagreement is currently more useful as a market-strength warning than as a bet-against-market signal. |
| locked_market_strength_underdog_log_c1_edge05 | market_too_strong_against_model_underdog | -58.5% | 45.1% | +34.6% | 20 | Model disagreement is currently more useful as a market-strength warning than as a bet-against-market signal. |
| locked_market_favorite_holds_edge05 | market_favorite_holds_despite_model_warning | -7.5% | 17.2% | +6.7% | 84 | Model disagreement is currently more useful as a market-strength warning than as a bet-against-market signal. |
| locked_decision_market_strength_conf62 | decision_market_strength_after_model_filter | -6.9% | 10.7% | +0.3% | 26 | Model-filtered decision rows show positive prop-market ROI; evaluate with a locked future slice. |
| locked_finish_proxy_conf62 | avoid_finish_edge_until_method_props_improve | -26.0% | -18.4% | -28.9% | 53 | Finish/inside-distance is the closest configured model candidate, but current prop-backed ROI is still negative. |

## Recommendation

- Status: `research_only`
- Reason: locked_finish_proxy_conf62 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
