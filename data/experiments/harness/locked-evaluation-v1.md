# Market Experiment Harness

- Generated: `2026-05-13T00:50:54.048103+00:00`
- Config: `configs/experiments/locked-evaluation-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 10
- Model-eligible fights: 104

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | original_winner_allresearch_c2p5_temp2p2_blend45_conf63 | +0.0% | 0.0182 | 0.0065 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | top_additional_allresearch_c2p0_temp2p2_blend55_conf66 | +0.0% | 0.0219 | 0.0080 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 3 | top_marketctx_c1p0_temp2p4_blend60_conf66 | +0.0% | 0.0312 | 0.0112 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 4 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 104 | 74.0% | 0.5608 | 0.1885 | 8.3% |
| original_winner_allresearch_c2p5_temp2p2_blend45_conf63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 59 | 81.4% | 0.5053 | 0.1617 | 6.7% |
| top_additional_allresearch_c2p0_temp2p2_blend55_conf66 | logistic_regression | production_plus_all_research_market_context | 0.55 | 49 | 81.6% | 0.5015 | 0.1601 | 4.6% |
| top_marketctx_c1p0_temp2p4_blend60_conf66 | logistic_regression | production_plus_market_context | 0.6 | 37 | 81.1% | 0.5049 | 0.1615 | 0.6% |

## Recommendation

- Status: `research_only`
- Reason: original_winner_allresearch_c2p5_temp2p2_blend45_conf63 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
