# Market Residual Bucket Report

- Generated: `2026-05-12T05:48:36.432964+00:00`
- Value status: `research_only`
- Scored events: 51
- Scored fights: 486
- Writes `model_versions`: `false`
- Input baseline: `data/experiments/market-residual-analysis-baseline.json`

## Unstable Bucket Policy

Buckets with fewer than 30 fights or fewer than 5 events are flagged unstable and excluded from promotion recommendations.

## Overall

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 379 | 40 | true | 52.0% | 74.7% | -8.9% | 18.5% | -27.4% | 0.7266 | 0.5766 | 0.2641 | 0.1952 | -9.1% | +9.5% |

## Favorite/Underdog Side

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| model_on_market_favorite | 233 | 40 | true | 71.7% | 71.7% | 11.6% | 11.6% | +0.0% | 0.6310 | 0.5888 | 0.2195 | 0.2010 | +10.2% | +6.0% |
| model_on_market_underdog | 146 | 39 | true | 20.5% | 79.5% | -41.7% | 29.5% | -71.1% | 0.8790 | 0.5572 | 0.3353 | 0.1861 | -39.8% | +15.0% |

## Odds Range

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| favorite_55_65 | 157 | 38 | true | 49.0% | 70.1% | -8.2% | 20.1% | -28.3% | 0.7467 | 0.6268 | 0.2747 | 0.2173 | -12.1% | +9.9% |
| heavy_favorite_75_plus | 64 | 32 | true | 64.1% | 87.5% | -9.8% | 11.0% | -20.8% | 0.6653 | 0.3915 | 0.2339 | 0.1139 | +1.6% | +6.8% |
| near_pickem_50_55 | 51 | 29 | true | 47.1% | 74.5% | -10.8% | 45.5% | -56.3% | 0.7441 | 0.6683 | 0.2730 | 0.2376 | -13.1% | +22.2% |
| strong_favorite_65_75 | 107 | 38 | true | 51.4% | 73.8% | -8.5% | 7.7% | -16.2% | 0.7252 | 0.5700 | 0.2625 | 0.1912 | -9.1% | +4.2% |

## Weight Class

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bantamweight | 45 | 26 | true | 55.6% | 80.0% | -14.3% | 18.2% | -32.5% | 0.6917 | 0.5322 | 0.2493 | 0.1745 | -7.0% | +13.5% |
| catch weight | 5 | 5 | false | 80.0% | 80.0% | 40.8% | 74.7% | -33.9% | 0.5644 | 0.4954 | 0.1917 | 0.1622 | +19.3% | +14.7% |
| featherweight | 43 | 28 | true | 53.5% | 65.1% | 7.4% | 1.8% | +5.6% | 0.7332 | 0.6129 | 0.2665 | 0.2143 | -6.8% | +0.2% |
| flyweight | 30 | 20 | true | 56.7% | 73.3% | -17.5% | 39.2% | -56.7% | 0.6716 | 0.5775 | 0.2405 | 0.1975 | -4.6% | +7.2% |
| heavyweight | 25 | 19 | false | 40.0% | 84.0% | -33.3% | 22.7% | -56.0% | 0.7850 | 0.4915 | 0.2902 | 0.1563 | -21.6% | +18.5% |
| light heavyweight | 25 | 20 | false | 28.0% | 68.0% | -57.5% | 4.4% | -61.9% | 0.8505 | 0.5798 | 0.3229 | 0.1967 | -30.4% | +6.0% |
| lightweight | 52 | 32 | true | 55.8% | 75.0% | -12.8% | 9.9% | -22.8% | 0.7313 | 0.5830 | 0.2651 | 0.1981 | -6.9% | +8.5% |
| middleweight | 41 | 26 | true | 53.7% | 80.5% | -6.0% | 19.1% | -25.2% | 0.6795 | 0.5728 | 0.2428 | 0.1905 | -6.3% | +13.5% |
| welterweight | 49 | 32 | true | 53.1% | 69.4% | -11.9% | 6.8% | -18.7% | 0.7171 | 0.6203 | 0.2585 | 0.2142 | -6.5% | +5.7% |
| women's bantamweight | 16 | 13 | false | 43.8% | 81.2% | 10.1% | 50.4% | -40.3% | 0.7377 | 0.5618 | 0.2696 | 0.1873 | -19.3% | +17.3% |
| women's featherweight | 3 | 3 | false | 66.7% | 100.0% | 18.1% | 71.8% | -53.8% | 0.6844 | 0.5590 | 0.2456 | 0.1836 | +12.5% | +42.7% |
| women's flyweight | 22 | 20 | false | 68.2% | 63.6% | 63.0% | 29.8% | +33.2% | 0.6942 | 0.6354 | 0.2483 | 0.2237 | +7.3% | +0.2% |
| women's strawweight | 23 | 20 | false | 43.5% | 82.6% | -24.6% | 25.0% | -49.6% | 0.8130 | 0.5564 | 0.3051 | 0.1865 | -19.0% | +16.7% |

## Event Date Age

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| last_12_months | 379 | 40 | true | 52.0% | 74.7% | -8.9% | 18.5% | -27.4% | 0.7266 | 0.5766 | 0.2641 | 0.1952 | -9.1% | +9.5% |

## Feature Availability

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| complete | 226 | 40 | true | 54.0% | 71.7% | -6.3% | 11.8% | -18.2% | 0.7011 | 0.5948 | 0.2527 | 0.2032 | -5.8% | +6.4% |
| mostly_complete | 89 | 37 | true | 46.1% | 77.5% | -13.7% | 31.0% | -44.7% | 0.7616 | 0.5637 | 0.2816 | 0.1890 | -15.3% | +13.8% |
| sparse | 64 | 30 | true | 53.1% | 81.2% | -11.4% | 24.5% | -35.9% | 0.7676 | 0.5302 | 0.2802 | 0.1757 | -11.8% | +14.3% |

## Confidence

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| model_50_55 | 95 | 37 | true | 48.4% | 72.6% | -11.4% | 12.2% | -23.5% | 0.6977 | 0.5871 | 0.2523 | 0.2010 | -4.1% | +7.7% |
| model_55_60 | 96 | 39 | true | 52.1% | 77.1% | -10.3% | 30.5% | -40.7% | 0.6971 | 0.5665 | 0.2520 | 0.1901 | -5.1% | +12.8% |
| model_60_65 | 86 | 36 | true | 59.3% | 75.6% | -2.1% | 15.1% | -17.3% | 0.6782 | 0.5714 | 0.2425 | 0.1923 | -3.0% | +10.4% |
| model_65_70 | 49 | 29 | true | 51.0% | 71.4% | 3.1% | 20.5% | -17.4% | 0.7508 | 0.6019 | 0.2769 | 0.2054 | -16.1% | +4.5% |
| model_70_plus | 53 | 25 | true | 47.2% | 75.5% | -24.2% | 11.6% | -35.8% | 0.8876 | 0.5611 | 0.3308 | 0.1895 | -28.3% | +9.5% |

## Market/Model Disagreement

| Bucket | Fights | Events | Stable | Model acc | Market acc | Model ROI | Market ROI | ROI delta | Model log loss | Market log loss | Model Brier | Market Brier | Model cal gap | Market cal gap |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| agree_delta_0_5pp | 74 | 35 | true | 71.6% | 71.6% | 12.9% | 12.9% | +0.0% | 0.6126 | 0.6073 | 0.2109 | 0.2085 | +10.2% | +10.2% |
| agree_delta_10_20pp | 72 | 38 | true | 69.4% | 69.4% | -1.3% | -1.3% | +0.0% | 0.6483 | 0.5942 | 0.2274 | 0.2029 | +7.7% | -0.0% |
| agree_delta_20pp_plus | 23 | 16 | false | 95.7% | 95.7% | 24.9% | 24.9% | +0.0% | 0.5151 | 0.3548 | 0.1680 | 0.0977 | +34.3% | +19.8% |
| agree_delta_5_10pp | 64 | 35 | true | 65.6% | 65.6% | 19.9% | 19.9% | +0.0% | 0.6746 | 0.6454 | 0.2392 | 0.2272 | +4.4% | +2.8% |
| disagree_delta_0_5pp | 7 | 7 | false | 28.6% | 71.4% | -42.1% | 73.8% | -115.9% | 0.7065 | 0.6781 | 0.2567 | 0.2425 | -22.7% | +19.4% |
| disagree_delta_10_20pp | 33 | 22 | true | 21.2% | 78.8% | -45.8% | 26.5% | -72.3% | 0.7705 | 0.5873 | 0.2881 | 0.1982 | -34.6% | +18.4% |
| disagree_delta_20pp_plus | 95 | 37 | true | 18.9% | 81.1% | -40.1% | 26.8% | -66.9% | 0.9471 | 0.5262 | 0.3655 | 0.1724 | -44.5% | +13.2% |
| disagree_delta_5_10pp | 11 | 10 | false | 27.3% | 72.7% | -42.3% | 32.8% | -75.1% | 0.7269 | 0.6572 | 0.2668 | 0.2321 | -25.6% | +18.0% |

## Policy

Residual buckets are diagnostic research artifacts only. They do not activate value status, publish betting claims, write model_versions, or create promotion recommendations.
