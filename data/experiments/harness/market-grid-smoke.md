# Market Experiment Harness

- Generated: `2026-05-12T06:19:48.803990+00:00`
- Config: `configs/experiments/market-grid.example.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | blend_25_availability_75_market | -6.9% | 0.0239 | 0.0103 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 2 | blend_25_xgboost_75_market | -8.0% | 0.0230 | 0.0099 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 3 | blend_50_xgboost_50_market | -12.3% | 0.0544 | 0.0247 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | xgboost_availability | -23.9% | 0.1525 | 0.0701 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 5 | xgboost_production | -27.4% | 0.1500 | 0.0689 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 6 | logistic_production | -27.7% | 0.2934 | 0.1079 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 7 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgboost_production | xgboost | production |  | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgboost_availability | xgboost | production_plus_availability |  | 379 | 53.8% | 0.7291 | 0.2653 | -5.5% |
| logistic_production | logistic_regression | production |  | 379 | 50.4% | 0.8700 | 0.3031 | -9.2% |
| blend_25_xgboost_75_market | xgboost | production | 0.25 | 379 | 70.7% | 0.5995 | 0.2052 | 10.5% |
| blend_50_xgboost_50_market | xgboost | production | 0.5 | 379 | 66.5% | 0.6310 | 0.2200 | 6.2% |
| blend_25_availability_75_market | xgboost | production_plus_availability | 0.25 | 379 | 71.0% | 0.6005 | 0.2056 | 11.6% |

## Recommendation

- Status: `research_only`
- Reason: blend_25_availability_75_market is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
