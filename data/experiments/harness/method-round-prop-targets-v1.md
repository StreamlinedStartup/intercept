# Market Experiment Harness

- Generated: `2026-05-16T04:48:51.327607+00:00`
- Config: `configs/experiments/method-round-prop-targets-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 70
- Model-eligible fights: 683

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | over_4_5_positive_log_c1_conf50 | +46.1% | 0.6409 | 0.2192 | false | log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | over_2_5_positive_log_c1_conf58 | +21.9% | -0.0024 | -0.0057 | true |  |
| 3 | over_3_5_positive_log_c1_conf54 | +0.0% | 0.5314 | 0.2036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 4 | finish_positive_log_c1_conf62 | -0.3% | 0.1457 | 0.0521 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 5 | over_1_5_positive_log_c1_conf62 | -3.2% | 0.0349 | 0.0097 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 6 | decision_positive_log_c1_conf62 | -17.5% | 0.1576 | 0.0668 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 7 | submission_positive_log_c1_conf22 | -27.3% | 0.5661 | 0.2377 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 8 | ko_tko_positive_log_c1_conf32 | -30.3% | 0.1660 | 0.0750 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 9 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Target Market Coverage

| Target | Label rows | Market rows | Market coverage | Status |
|---|---:|---:|---:|---|
| decision | 683 | 316 | 46.3% | market_backed |
| finish | 683 | 316 | 46.3% | market_backed |
| ko_tko | 683 | 316 | 46.3% | market_backed |
| over_1_5 | 683 | 316 | 46.3% | market_backed |
| over_2_5 | 683 | 316 | 46.3% | market_backed |
| over_3_5 | 683 | 29 | 4.2% | market_backed |
| over_4_5 | 683 | 30 | 4.4% | market_backed |
| submission | 683 | 316 | 46.3% | market_backed |

## Variants

| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | winner | market_favorite | none |  | 683 | 72.8% | 0.5819 | 0.1981 | 11.5% |
| decision_positive_log_c1_conf62 | decision | logistic_regression | production_plus_all_research |  | 143 | 55.2% | 0.7680 | 0.2769 | -2.7% |
| finish_positive_log_c1_conf62 | finish | logistic_regression | production_plus_all_research |  | 174 | 54.6% | 0.7801 | 0.2758 | -14.2% |
| ko_tko_positive_log_c1_conf32 | ko_tko | logistic_regression | production_plus_all_research |  | 128 | 41.4% | 0.7648 | 0.2807 | -14.8% |
| submission_positive_log_c1_conf22 | submission | logistic_regression | production_plus_all_research |  | 66 | 18.2% | 1.0601 | 0.3950 | -15.1% |
| over_1_5_positive_log_c1_conf62 | over_1_5 | logistic_regression | production_plus_all_research |  | 490 | 77.6% | 0.5515 | 0.1780 | 7.9% |
| over_2_5_positive_log_c1_conf58 | over_2_5 | logistic_regression | production_plus_all_research |  | 450 | 73.8% | 0.6012 | 0.2015 | 33.3% |
| over_3_5_positive_log_c1_conf54 | over_3_5 | logistic_regression | production_plus_all_research |  | 37 | 35.1% | 0.9318 | 0.3172 | 51.1% |
| over_4_5_positive_log_c1_conf50 | over_4_5 | logistic_regression | production_plus_all_research |  | 36 | 25.0% | 1.1390 | 0.3765 | 67.7% |

## Signal Diagnostics

| Variant | Indicator | Model ROI | Selected market ROI | Market ROI delta | Entries | Read |
|---|---|---:|---:|---:|---:|---|
| over_3_5_positive_log_c1_conf54 | no_positive_market_indicator | 51.1% | 51.1% | +39.6% | 5 | No actionable positive signal in this selected subset. |
| over_4_5_positive_log_c1_conf50 | no_positive_market_indicator | 67.7% | 21.5% | +10.0% | 5 | No actionable positive signal in this selected subset. |
| ko_tko_positive_log_c1_conf32 | no_positive_market_indicator | -14.8% | 15.5% | +4.0% | 59 | No actionable positive signal in this selected subset. |
| decision_positive_log_c1_conf62 | decision_market_strength_after_model_filter | -2.7% | 14.8% | +3.2% | 49 | Model-filtered decision rows show positive prop-market ROI; evaluate with a locked future slice. |
| submission_positive_log_c1_conf22 | no_positive_market_indicator | -15.1% | 12.3% | +0.7% | 13 | No actionable positive signal in this selected subset. |
| over_2_5_positive_log_c1_conf58 | no_positive_market_indicator | 33.3% | 11.4% | -0.1% | 203 | No actionable positive signal in this selected subset. |
| over_1_5_positive_log_c1_conf62 | no_positive_market_indicator | 7.9% | 11.0% | -0.5% | 215 | No actionable positive signal in this selected subset. |
| finish_positive_log_c1_conf62 | avoid_finish_edge_until_method_props_improve | -14.2% | -13.9% | -25.4% | 81 | Finish/inside-distance is the closest configured model candidate, but current prop-backed ROI is still negative. |

## Recommendation

- Status: `candidate_for_locked_evaluation`
- Reason: over_2_5_positive_log_c1_conf58 clears the configured discovery gate; evaluate on a locked future slice before activation.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
