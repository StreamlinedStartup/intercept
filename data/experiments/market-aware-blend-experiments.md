# Market-Aware Blend Experiments

- Generated: `2026-05-12T04:04:50.162163+00:00`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Scored events: 37
- Scored fights: 345

## Gate

- Market favorite ROI: 16.2%
- Best candidate: `blend_25_model_75_market`
- Best candidate ROI: 15.9%
- Delta vs market favorite: -0.3pp
- Candidate cleared +2pp gate: `false`

## Variants

| Variant | Family | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate |
|---|---|---:|---:|---:|---:|---:|---|
| market_favorite | baseline | 75.1% | 0.5707 | 0.1925 | 16.2% | +0.0pp | false |
| model_pick | model | 44.1% | 0.7348 | 0.2705 | -10.4% | -26.5pp | false |
| blend_10_model_90_market | blend | 73.6% | 0.5789 | 0.1959 | 13.4% | -2.7pp | false |
| blend_20_model_80_market | blend | 74.8% | 0.5891 | 0.2003 | 15.8% | -0.3pp | false |
| blend_25_model_75_market | blend | 74.8% | 0.5949 | 0.2029 | 15.9% | -0.3pp | false |
| blend_30_model_70_market | blend | 73.6% | 0.6011 | 0.2057 | 13.8% | -2.3pp | false |
| blend_40_model_60_market | blend | 71.6% | 0.6148 | 0.2121 | 10.8% | -5.4pp | false |
| blend_50_model_50_market | blend | 68.1% | 0.6302 | 0.2194 | 5.9% | -10.3pp | false |
| blend_60_model_40_market | blend | 62.6% | 0.6473 | 0.2277 | -1.6% | -17.7pp | false |
| blend_70_model_30_market | blend | 56.5% | 0.6662 | 0.2369 | -2.4% | -18.6pp | false |
| blend_75_model_25_market | blend | 49.6% | 0.6763 | 0.2419 | -7.8% | -23.9pp | false |
| blend_80_model_20_market | blend | 47.2% | 0.6869 | 0.2471 | -6.1% | -22.3pp | false |
| blend_90_model_10_market | blend | 47.2% | 0.7098 | 0.2583 | -6.1% | -22.3pp | false |
| model_shrink_25 | calibration | 44.1% | 0.7207 | 0.2636 | -10.4% | -26.5pp | false |
| model_shrink_50 | calibration | 44.1% | 0.7091 | 0.2579 | -10.4% | -26.5pp | false |
| model_shrink_75 | calibration | 44.1% | 0.7000 | 0.2534 | -10.4% | -26.5pp | false |
| blend_25_model_75_market_shrink_25 | calibrated_blend | 74.8% | 0.6138 | 0.2113 | 15.9% | -0.3pp | false |
| blend_25_model_75_market_shrink_50 | calibrated_blend | 74.8% | 0.6363 | 0.2219 | 15.9% | -0.3pp | false |

## Policy

Calibration and blend variants are report-only until a candidate beats the no-vig market favorite by the configured ROI gate.
This experiment does not save model files, write `model_versions`, or activate value claims.
