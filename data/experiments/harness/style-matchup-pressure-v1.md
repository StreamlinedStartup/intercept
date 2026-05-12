# Market Experiment Harness

- Generated: `2026-05-12T23:06:12.706530+00:00`
- Config: `configs/experiments/style-matchup-pressure-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | xgb_style_matchup_pressure_blend_10 | -3.3% | 0.0090 | 0.0037 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 2 | xgb_style_matchup_pressure | -27.2% | 0.1569 | 0.0725 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 3 | xgb_current | -27.4% | 0.1500 | 0.0689 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgb_current | xgboost | production |  | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgb_style_matchup_pressure | xgboost | production_plus_style_matchup_pressure |  | 379 | 52.5% | 0.7335 | 0.2677 | -8.8% |
| xgb_style_matchup_pressure_blend_10 | xgboost | production_plus_style_matchup_pressure | 0.1 | 379 | 73.4% | 0.5856 | 0.1990 | 15.2% |

## Recommendation

- Status: `research_only`
- Reason: xgb_style_matchup_pressure_blend_10 is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
