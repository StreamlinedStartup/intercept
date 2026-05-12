# Market-Aware Blend Experiments

- Generated: `2026-05-12T04:39:11.757737+00:00`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Scored events: 51
- Scored fights: 486

## Gate

- Market favorite ROI: 20.0%
- Best candidate: `blend_25_model_75_market`
- Best candidate ROI: 18.5%
- Delta vs market favorite: -1.5pp
- Candidate cleared +2pp gate: `false`

## Variants

| Variant | Family | Accuracy | Log loss | Brier | ROI | Delta vs market | Clears gate |
|---|---|---:|---:|---:|---:|---:|---|
| market_favorite | baseline | 75.1% | 0.5684 | 0.1916 | 20.0% | +0.0pp | false |
| model_pick | model | 44.0% | 0.7331 | 0.2697 | -11.2% | -31.2pp | false |
| blend_10_model_90_market | blend | 73.5% | 0.5769 | 0.1951 | 16.7% | -3.2pp | false |
| blend_20_model_80_market | blend | 74.3% | 0.5873 | 0.1995 | 18.4% | -1.5pp | false |
| blend_25_model_75_market | blend | 74.3% | 0.5932 | 0.2021 | 18.5% | -1.5pp | false |
| blend_30_model_70_market | blend | 73.3% | 0.5994 | 0.2049 | 16.7% | -3.3pp | false |
| blend_40_model_60_market | blend | 71.2% | 0.6132 | 0.2112 | 13.5% | -6.4pp | false |
| blend_50_model_50_market | blend | 68.5% | 0.6286 | 0.2185 | 10.1% | -9.9pp | false |
| blend_60_model_40_market | blend | 64.2% | 0.6457 | 0.2268 | 5.2% | -14.8pp | false |
| blend_70_model_30_market | blend | 58.0% | 0.6646 | 0.2361 | 3.3% | -16.6pp | false |
| blend_75_model_25_market | blend | 51.2% | 0.6747 | 0.2411 | -1.7% | -21.7pp | false |
| blend_80_model_20_market | blend | 48.1% | 0.6853 | 0.2463 | -4.0% | -24.0pp | false |
| blend_90_model_10_market | blend | 47.9% | 0.7081 | 0.2575 | -4.3% | -24.2pp | false |
| model_shrink_25 | calibration | 44.0% | 0.7194 | 0.2630 | -11.2% | -31.2pp | false |
| model_shrink_50 | calibration | 44.0% | 0.7083 | 0.2575 | -11.2% | -31.2pp | false |
| model_shrink_75 | calibration | 44.0% | 0.6995 | 0.2532 | -11.2% | -31.2pp | false |
| blend_25_model_75_market_shrink_25 | calibrated_blend | 74.3% | 0.6124 | 0.2106 | 18.5% | -1.5pp | false |
| blend_25_model_75_market_shrink_50 | calibrated_blend | 74.3% | 0.6354 | 0.2215 | 18.5% | -1.5pp | false |

## Policy

Calibration and blend variants are report-only until a candidate beats the no-vig market favorite by the configured ROI gate.
This experiment does not save model files, write `model_versions`, or activate value claims.
