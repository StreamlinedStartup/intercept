# Market Gate Report

- Generated: `2026-05-12T03:07:42.748643+00:00`
- Value status: `insufficient_coverage`
- Reason: Only 235 matched fights across 26 events were scored; need at least 200 fights across 30 events.
- Scored events: 26
- Scored fights: 235
- Moneyline rows linked: 13759/23598
- Writes `model_versions`: `false`

## Strategy Comparison

| Strategy | Count | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| model_pick | 235 | 42.6% | 59.1% | -16.6% | 0.7368 | 0.2715 | 0.4320 | -12.5% |
| market_favorite | 235 | 75.3% | 66.6% | +8.7% | 0.5616 | 0.1886 | 0.7916 | 12.9% |
| blend_50_50 | 235 | 68.9% | 58.0% | +10.9% | 0.6241 | 0.2165 | 0.7462 | 3.3% |
| blend_25_model_75_market | 235 | 76.2% | 62.0% | +14.1% | 0.5865 | 0.1992 | 0.7854 | 14.9% |
| blend_75_model_25_market | 235 | 50.2% | 56.3% | -6.1% | 0.6736 | 0.2406 | 0.5829 | -8.7% |

## Timestamp Semantics

FightOdds source_current lines are captured at import scrape time. This report uses them as current/consensus market probabilities only, not as true closing-line value.

## Policy

This report is a market gate, not a promotion. A validated value status requires enough matched market history and a durable improvement over the market baseline.
