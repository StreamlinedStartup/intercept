# Market Residual Failure Clusters

- Generated: `2026-05-12T05:52:20.002490+00:00`
- Value status: `research_only`
- Model-eligible events: 40
- Model-eligible fights: 379
- Writes `model_versions`: `false`
- Input report: `data/experiments/market-residual-buckets.json`

## High-Loss Clusters

| Cluster | Fights | Events | Model acc | Market acc | ROI delta | High-conf wrong | Explanation | Actionable gaps |
|---|---:|---:|---:|---:|---:|---:|---|---|
| market_model_disagreement:disagree_delta_0_5pp | 7 | 7 | 28.6% | 71.4% | -115.9% | 0.0% | unstable_or_noise | none |
| market_model_disagreement:disagree_delta_5_10pp | 11 | 10 | 27.3% | 72.7% | -75.1% | 0.0% | unstable_or_noise | none |
| market_model_disagreement:disagree_delta_10_20pp | 33 | 22 | 21.2% | 78.8% | -72.3% | 3.0% | market_prior_gap | none |
| favorite_underdog_side:model_on_market_underdog | 146 | 39 | 20.5% | 79.5% | -71.1% | 21.2% | market_prior_gap | none |
| market_model_disagreement:disagree_delta_20pp_plus | 95 | 37 | 18.9% | 81.1% | -66.9% | 31.6% | market_prior_gap | none |
| weight_class:light heavyweight | 25 | 20 | 28.0% | 68.0% | -61.9% | 24.0% | unstable_or_noise | none |
| weight_class:flyweight | 30 | 20 | 56.7% | 73.3% | -56.7% | 10.0% | model_calibration_or_noise | none |
| odds_range:near_pickem_50_55 | 51 | 29 | 47.1% | 74.5% | -56.3% | 17.6% | model_calibration_or_noise | none |
| weight_class:heavyweight | 25 | 19 | 40.0% | 84.0% | -56.0% | 12.0% | unstable_or_noise | none |
| weight_class:women's featherweight | 3 | 3 | 66.7% | 100.0% | -53.8% | 0.0% | unstable_or_noise | none |
| weight_class:women's strawweight | 23 | 20 | 43.5% | 82.6% | -49.6% | 21.7% | unstable_or_noise | none |
| feature_availability:mostly_complete | 89 | 37 | 46.1% | 77.5% | -44.7% | 18.0% | model_calibration_or_noise | none |
| confidence:model_55_60 | 96 | 39 | 52.1% | 77.1% | -40.7% | 0.0% | model_calibration_or_noise | none |
| weight_class:women's bantamweight | 16 | 13 | 43.8% | 81.2% | -40.3% | 18.8% | unstable_or_noise | higher_feature_missingness, lower_has_recent_form |
| feature_availability:sparse | 64 | 30 | 53.1% | 81.2% | -35.9% | 23.4% | actionable_pre_fight_feature_gap | higher_feature_missingness, lower_has_recent_form |
| confidence:model_70_plus | 53 | 25 | 47.2% | 75.5% | -35.8% | 52.8% | actionable_pre_fight_feature_gap | higher_feature_missingness, lower_has_recent_form |
| weight_class:catch weight | 5 | 5 | 80.0% | 80.0% | -33.9% | 0.0% | unstable_or_noise | higher_feature_missingness, lower_has_recent_form |
| weight_class:bantamweight | 45 | 26 | 55.6% | 80.0% | -32.5% | 15.6% | model_calibration_or_noise | none |
| odds_range:favorite_55_65 | 157 | 38 | 49.0% | 70.1% | -28.3% | 15.9% | model_calibration_or_noise | none |
| event_date_age:last_12_months | 379 | 40 | 52.0% | 74.7% | -27.4% | 13.7% | model_calibration_or_noise | none |
| weight_class:middleweight | 41 | 26 | 53.7% | 80.5% | -25.2% | 9.8% | model_calibration_or_noise | none |
| confidence:model_50_55 | 95 | 37 | 48.4% | 72.6% | -23.5% | 0.0% | model_calibration_or_noise | none |
| odds_range:heavy_favorite_75_plus | 64 | 32 | 64.1% | 87.5% | -20.8% | 12.5% | actionable_pre_fight_feature_gap | higher_feature_missingness, lower_has_recent_form |
| confidence:model_65_70 | 49 | 29 | 51.0% | 71.4% | -17.4% | 49.0% | model_calibration_or_noise | none |
| odds_range:strong_favorite_65_75 | 107 | 38 | 51.4% | 73.8% | -16.2% | 9.3% | model_calibration_or_noise | none |

## Feature Baseline

- Corpus average missing rate: 9.5%
- Corpus recent-form availability: 83.1%
- Corpus physical-profile availability: 100.0%
- Corpus weight-context availability: 98.2%
- Corpus common-opponent availability: 100.0%

## Recommendation Policy

Only stable clusters with actionable pre-fight feature gaps can feed Task D signal candidates. Market-only and unstable/noise clusters are diagnostic only.
This report does not write model_versions or activate betting/value claims.
