# Market-Aware Model-Family Experiments

- Generated: `2026-05-12T06:02:44.026370+00:00`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Scored events: 51
- Scored fights: 486
- Model-eligible events: 40
- Model-eligible fights: 379

## Gate

- Market favorite ROI: 18.5%
- Best candidate: `blend_25_xgboost_75_market`
- Best candidate ROI: 10.5%
- Delta vs market favorite: -8.0pp
- Candidate cleared +2pp gate: `false`
- Rejection reasons: roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market

## Variants

| Variant | Family | Events | Fights | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate | Rejection reasons |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| market_favorite | market_baseline | 40 | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% | +0.0pp | false | baseline_not_candidate |
| xgboost_current | current_model_baseline | 40 | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% | -27.4pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| blend_25_xgboost_75_market | market_aware_blend | 40 | 379 | 70.7% | 0.5995 | 0.2052 | 10.5% | -8.0pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| blend_50_xgboost_50_market | market_aware_blend | 40 | 379 | 66.5% | 0.6310 | 0.2200 | 6.2% | -12.3pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| logistic_current | model_family | 40 | 379 | 50.4% | 0.8700 | 0.3031 | -9.2% | -27.7pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_recent_form | feature_ablation | 40 | 379 | 52.2% | 0.7307 | 0.2659 | -9.1% | -27.6pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| xgboost_no_damage | feature_ablation | 40 | 379 | 51.2% | 0.7238 | 0.2632 | -10.0% | -28.4pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_common_opponents | feature_ablation | 40 | 379 | 53.0% | 0.7280 | 0.2650 | -7.5% | -26.0pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| xgboost_no_stance | feature_ablation | 40 | 379 | 54.4% | 0.7337 | 0.2671 | -4.5% | -23.0pp | false | roi_delta_below_plus_2pp_market_gate, log_loss_worse_than_market, brier_worse_than_market |

## Policy

Model-family and feature-ablation candidates remain research-only until a candidate beats the no-vig market favorite by +2pp without leakage, instability, or calibration degradation.
This experiment does not save model files, write `model_versions`, or activate value claims.
