# Market Experiment Harness

- Generated: `2026-05-12T22:53:25.974499+00:00`
- Config: `configs/experiments/opponent-adjusted-recent-performance-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | xgb_opponent_adjusted_recent_performance_blend_10 | -3.2% | 0.0085 | 0.0035 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 2 | xgb_opponent_adjusted_recent_performance | -26.7% | 0.1501 | 0.0691 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 3 | xgb_current | -27.4% | 0.1500 | 0.0689 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgb_current | xgboost | production |  | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgb_opponent_adjusted_recent_performance | xgboost | production_plus_opponent_adjusted_recent_performance |  | 379 | 53.8% | 0.7267 | 0.2643 | -8.2% |
| xgb_opponent_adjusted_recent_performance_blend_10 | xgboost | production_plus_opponent_adjusted_recent_performance | 0.1 | 379 | 73.1% | 0.5851 | 0.1988 | 15.3% |

## Recommendation

- Status: `research_only`
- Reason: xgb_opponent_adjusted_recent_performance_blend_10 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
