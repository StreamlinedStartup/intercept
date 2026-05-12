# Market Gate Report

- Generated: `2026-05-12T01:23:23.545952+00:00`
- Value status: `insufficient_coverage`
- Reason: Only 30 matched fights across 3 events were scored; need at least 200 fights across 30 events.
- Scored events: 3
- Scored fights: 30
- Moneyline rows linked: 1553/2173
- Writes `model_versions`: `false`

## Strategy Comparison

| Strategy | Count | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| model_pick | 30 | 36.7% | 59.0% | -22.3% | 0.7588 | 0.2823 | 0.3711 | -16.4% |
| market_favorite | 30 | 76.7% | 70.1% | +6.6% | 0.5166 | 0.1685 | 0.8356 | 7.2% |
| blend_50_50 | 30 | 70.0% | 58.9% | +11.1% | 0.6024 | 0.2064 | 0.7911 | -3.8% |
| blend_25_model_75_market | 30 | 76.7% | 64.3% | +12.3% | 0.5500 | 0.1827 | 0.8356 | 7.2% |
| blend_75_model_25_market | 30 | 46.7% | 55.7% | -9.0% | 0.6712 | 0.2396 | 0.5511 | -21.9% |

## Timestamp Semantics

FightOdds source_current lines are captured at import scrape time. This report uses them as current/consensus market probabilities only, not as true closing-line value.

## Policy

This report is a market gate, not a promotion. A validated value status requires enough matched market history and a durable improvement over the market baseline.
