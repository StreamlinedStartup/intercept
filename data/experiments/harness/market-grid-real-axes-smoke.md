# Market Experiment Harness

- Generated: `2026-05-12T22:24:54.893673+00:00`
- Config: `configs/experiments/market-grid-real-axes-smoke.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | logistic_c_025_temperature_150_blend_10 | -3.7% | 0.0075 | 0.0031 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 2 | xgb_temperature_150_blend_25 | -4.1% | 0.0212 | 0.0090 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 3 | xgb_availability_shallow_blend_25 | -6.0% | 0.0221 | 0.0095 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | logistic_core_stats_only | -21.8% | 0.1589 | 0.0685 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 5 | xgb_temperature_150 | -27.4% | 0.1301 | 0.0609 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 6 | xgb_default | -27.4% | 0.1500 | 0.0689 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 7 | xgb_no_recent_form | -27.6% | 0.1541 | 0.0707 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 8 | logistic_default | -27.7% | 0.2934 | 0.1079 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 9 | xgb_shallow | -29.8% | 0.1374 | 0.0637 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 10 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgb_default | xgboost | production |  | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgb_shallow | xgboost | production |  | 379 | 51.7% | 0.7140 | 0.2590 | -11.3% |
| xgb_no_recent_form | xgboost | production |  | 379 | 52.2% | 0.7307 | 0.2659 | -9.1% |
| xgb_temperature_150 | xgboost | production |  | 379 | 52.0% | 0.7067 | 0.2562 | -8.9% |
| xgb_temperature_150_blend_25 | xgboost | production | 0.25 | 379 | 72.6% | 0.5978 | 0.2043 | 14.4% |
| xgb_availability_shallow_blend_25 | xgboost | production_plus_availability | 0.25 | 379 | 71.5% | 0.5987 | 0.2048 | 12.5% |
| logistic_default | logistic_regression | production |  | 379 | 50.4% | 0.8700 | 0.3031 | -9.2% |
| logistic_c_025_temperature_150_blend_10 | logistic_regression | production | 0.1 | 379 | 72.8% | 0.5841 | 0.1983 | 14.8% |
| logistic_core_stats_only | logistic_regression | production |  | 379 | 55.1% | 0.7355 | 0.2638 | -3.3% |

## Recommendation

- Status: `research_only`
- Reason: logistic_c_025_temperature_150_blend_10 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
