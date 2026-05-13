# Market Experiment Harness

- Generated: `2026-05-13T00:23:47.305507+00:00`
- Config: `configs/experiments/winner-expanded-corpus-mintrain-80.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 42
- Model-eligible fights: 397

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | +3.4% | -0.0014 | -0.0015 | true |  |
| 2 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 397 | 73.8% | 0.5794 | 0.1966 | 16.8% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 217 | 76.0% | 0.5463 | 0.1811 | 15.7% |

## Recommendation

- Status: `candidate_for_locked_evaluation`
- Reason: log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 clears the configured discovery gate; evaluate on a locked future slice before activation.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
