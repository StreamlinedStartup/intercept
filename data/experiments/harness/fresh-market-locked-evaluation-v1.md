# Market Experiment Harness

- Generated: `2026-05-13T01:09:20.494264+00:00`
- Config: `configs/experiments/fresh-market-locked-evaluation-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 30
- Model-eligible fights: 304

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | original_winner_allresearch_c2p5_temp2p2_blend45_conf63 | +0.0% | 0.0129 | 0.0045 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | top_additional_allresearch_c2p0_temp2p2_blend55_conf66 | +0.0% | 0.0147 | 0.0046 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 3 | top_marketctx_c1p0_temp2p4_blend60_conf66 | +0.0% | 0.0211 | 0.0066 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 4 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 304 | 70.4% | 0.5885 | 0.2017 | 2.8% |
| original_winner_allresearch_c2p5_temp2p2_blend45_conf63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 164 | 73.8% | 0.5526 | 0.1850 | -3.2% |
| top_additional_allresearch_c2p0_temp2p2_blend55_conf66 | logistic_regression | production_plus_all_research_market_context | 0.55 | 129 | 76.0% | 0.5327 | 0.1757 | -2.4% |
| top_marketctx_c1p0_temp2p4_blend60_conf66 | logistic_regression | production_plus_market_context | 0.6 | 115 | 77.4% | 0.5221 | 0.1702 | -1.6% |

## Recommendation

- Status: `research_only`
- Reason: original_winner_allresearch_c2p5_temp2p2_blend45_conf63 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
