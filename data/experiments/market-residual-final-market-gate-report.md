# Market Gate Report

- Generated: `2026-05-12T06:00:16.405942+00:00`
- Value status: `research_only`
- Reason: Model ROI did not clear the market-favorite baseline gate.
- Scored events: 51
- Scored fights: 486
- Moneyline rows linked: 28038/40022
- Writes `model_versions`: `false`

## Strategy Comparison

| Strategy | Count | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| model_pick | 486 | 44.0% | 59.2% | -15.1% | 0.7331 | 0.2697 | 0.4413 | -11.2% |
| market_favorite | 486 | 75.1% | 65.5% | +9.6% | 0.5684 | 0.1916 | 0.7891 | 20.0% |
| blend_50_50 | 486 | 68.5% | 57.8% | +10.7% | 0.6286 | 0.2185 | 0.7441 | 10.1% |
| blend_25_model_75_market | 486 | 74.3% | 61.4% | +12.9% | 0.5932 | 0.2021 | 0.7815 | 18.5% |
| blend_75_model_25_market | 486 | 51.2% | 56.5% | -5.3% | 0.6747 | 0.2411 | 0.5938 | -1.7% |

## Timestamp Semantics

FightOdds source_current lines are captured at import scrape time. This report uses them as current/consensus market probabilities only, not as true closing-line value.

## Policy

This report is a market gate, not a promotion. A validated value status requires enough matched market history and a durable improvement over the market baseline.
