# Market Experiment Harness

- Generated: `2026-05-16T01:02:21.438159+00:00`
- Config: `configs/experiments/market-opportunity-matrix-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 70
- Model-eligible fights: 683

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | finish_edge_log_c1_conf62 | +0.0% | 0.3276 | 0.1434 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | winner_abstain_log_c1_conf55 | -7.1% | 0.0459 | 0.0224 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 3 | winner_overpriced_favorite_log_c1_edge05 | -21.8% | 0.1674 | 0.0724 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | winner_undervalued_underdog_log_c1_edge05 | -52.8% | 0.2766 | 0.1204 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 5 | decision_edge_log_c1_conf62 | -53.8% | 0.2838 | 0.1235 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 6 | winner_underdog_blend40_edge04 | -59.3% | 0.1057 | 0.0518 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 7 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | winner | market_favorite | none |  | 683 | 72.8% | 0.5819 | 0.1981 | 11.5% |
| winner_overpriced_favorite_log_c1_edge05 | winner | logistic_regression | production_plus_all_research_market_context |  | 271 | 59.4% | 0.7024 | 0.2493 | -5.1% |
| winner_undervalued_underdog_log_c1_edge05 | winner | logistic_regression | production_plus_all_research_market_context |  | 112 | 26.8% | 0.8972 | 0.3352 | -32.4% |
| winner_underdog_blend40_edge04 | winner | logistic_regression | production_plus_all_research_market_context | 0.4 | 40 | 27.5% | 0.7454 | 0.2758 | -34.7% |
| decision_edge_log_c1_conf62 | decision | logistic_regression | production_plus_all_research |  | 143 | 55.2% | 0.7680 | 0.2769 | -43.9% |
| finish_edge_log_c1_conf62 | finish | logistic_regression | production_plus_all_research |  | 174 | 54.6% | 0.7801 | 0.2758 | 57.2% |
| winner_abstain_log_c1_conf55 | winner | logistic_regression | production_plus_all_research_market_context |  | 56 | 50.0% | 0.6929 | 0.2499 | -4.9% |

## Recommendation

- Status: `research_only`
- Reason: finish_edge_log_c1_conf62 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
