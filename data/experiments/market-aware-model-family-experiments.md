# Market-Aware Model-Family Experiments

- Generated: `2026-05-12T04:14:29.256796+00:00`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Scored events: 37
- Scored fights: 345
- Model-eligible events: 26
- Model-eligible fights: 241

## Gate

- Market favorite ROI: 9.8%
- Best candidate: `blend_25_xgboost_75_market`
- Best candidate ROI: 3.5%
- Delta vs market favorite: -6.3pp
- Candidate cleared +2pp gate: `false`
- Rejection reasons: roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market

## Variants

| Variant | Family | Events | Fights | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate | Rejection reasons |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| market_favorite | market_baseline | 26 | 241 | 74.7% | 0.5639 | 0.1893 | 9.8% | +0.0pp | false | baseline_not_candidate |
| xgboost_current | current_model_baseline | 26 | 241 | 51.0% | 0.7392 | 0.2698 | -19.9% | -29.7pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| blend_25_xgboost_75_market | market_aware_blend | 26 | 241 | 71.4% | 0.5931 | 0.2022 | 3.5% | -6.3pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market |
| blend_50_xgboost_50_market | market_aware_blend | 26 | 241 | 64.3% | 0.6307 | 0.2199 | -7.1% | -16.9pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market |
| logistic_current | model_family | 26 | 241 | 51.5% | 0.9340 | 0.3173 | -11.9% | -21.7pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_recent_form | feature_ablation | 26 | 241 | 51.9% | 0.7319 | 0.2663 | -17.2% | -27.0pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_damage | feature_ablation | 26 | 241 | 53.5% | 0.7368 | 0.2684 | -13.2% | -23.0pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_common_opponents | feature_ablation | 26 | 241 | 50.6% | 0.7453 | 0.2723 | -19.5% | -29.2pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |
| xgboost_no_stance | feature_ablation | 26 | 241 | 50.6% | 0.7433 | 0.2718 | -20.8% | -30.6pp | false | roi_delta_below_plus_2pp_market_gate, unstable_coverage_bucket, log_loss_worse_than_market, brier_worse_than_market, calibration_worse_than_market |

## Policy

Model-family and feature-ablation candidates remain research-only until a candidate beats the no-vig market favorite by +2pp without leakage, instability, or calibration degradation.
This experiment does not save model files, write `model_versions`, or activate value claims.
