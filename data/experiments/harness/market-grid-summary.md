# Market Experiment Harness Initial Matrix Summary

- Source report: `data/experiments/harness/market-grid-smoke.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible corpus: 40 events, 379 fights
- Market favorite baseline ROI: 18.48%

## Matrix

- Market favorite baseline
- Current XGBoost production features
- Availability-augmented XGBoost
- Regularized logistic production-feature baseline
- 25/75 and 50/50 XGBoost-to-market blends

## Ranking Against Market Favorite

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate |
|---:|---|---:|---:|---:|---|
| 1 | blend_25_availability_75_market | -6.89pp | 0.0239 | 0.0103 | false |
| 2 | blend_25_xgboost_75_market | -7.97pp | 0.0230 | 0.0099 | false |
| 3 | blend_50_xgboost_50_market | -12.32pp | 0.0544 | 0.0247 | false |

The best configured candidate was `blend_25_availability_75_market`, but it underperformed the market favorite baseline on ROI, log loss, and Brier score. The harness output therefore stays report-only and `research_only`.
