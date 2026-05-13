# Market Experiment Harness

- Generated: `2026-05-13T00:23:15.835144+00:00`
- Config: `configs/experiments/winner-expanded-corpus-mintrain-40.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 46
- Model-eligible fights: 438

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | +2.1% | -0.0115 | -0.0057 | true |  |
| 2 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 438 | 74.4% | 0.5781 | 0.1959 | 18.9% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 251 | 77.3% | 0.5338 | 0.1755 | 19.9% |

## Recommendation

- Status: `candidate_for_locked_evaluation`
- Reason: log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 clears the configured discovery gate; evaluate on a locked future slice before activation.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
