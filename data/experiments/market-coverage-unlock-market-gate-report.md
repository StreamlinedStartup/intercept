# Market Gate Report

- Generated: `2026-05-12T03:49:50.021461+00:00`
- Value status: `research_only`
- Reason: Model ROI did not clear the market-favorite baseline gate.
- Scored events: 37
- Scored fights: 345
- Moneyline rows linked: 20075/29056
- Writes `model_versions`: `false`

## Strategy Comparison

| Strategy | Count | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| model_pick | 345 | 44.1% | 59.2% | -15.1% | 0.7348 | 0.2705 | 0.4380 | -10.4% |
| market_favorite | 345 | 75.1% | 65.6% | +9.5% | 0.5707 | 0.1925 | 0.7849 | 16.2% |
| blend_50_50 | 345 | 68.1% | 57.7% | +10.4% | 0.6302 | 0.2194 | 0.7375 | 5.9% |
| blend_25_model_75_market | 345 | 74.8% | 61.4% | +13.4% | 0.5949 | 0.2029 | 0.7786 | 15.9% |
| blend_75_model_25_market | 345 | 49.6% | 56.5% | -6.9% | 0.6763 | 0.2419 | 0.5836 | -7.8% |

## Timestamp Semantics

FightOdds source_current lines are captured at import scrape time. This report uses them as current/consensus market probabilities only, not as true closing-line value.

## Policy

This report is a market gate, not a promotion. A validated value status requires enough matched market history and a durable improvement over the market baseline.
