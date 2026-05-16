# Market-Aware Model-Improvement Recommendation

- Generated: `2026-05-12T04:15:32Z`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Activation allowed: `false`

## Recommendation

Do not activate a model or blend. Continue research-only work focused on expanding trainable market-covered history and improving pre-fight feature signal before any active `model_versions` write.

## Evidence

| Experiment | Best candidate | ROI | Delta vs market favorite | Gate cleared |
|---|---|---:|---:|---|
| Blend/calibration | `blend_25_model_75_market` | 15.9% | -0.3pp | false |
| Model-family/features | `blend_25_xgboost_75_market` | 3.5% | -6.3pp | false |

The frozen corpus has 345 scored fights across 37 market-covered events, so the broad coverage gate is met. The trainable model-family slice has 241 fights across 26 model-eligible events after requiring prior market-covered training fights, so it remains below the 30-event stability floor.

## Blockers

- No candidate beats the no-vig market favorite by the required +2pp simulated ROI gate.
- Current XGBoost, logistic regression, and conservative feature ablations degrade ROI and probability quality versus the market favorite.
- Trainable model experiments are still event-limited after enforcing prior-event training only.
- Validated/value UI, API, and docs claims remain blocked until a separate activation epic passes the gate.

## Next Recommended Epic

`D2-TMC: Trainable market-covered corpus expansion`

Goal: increase prior-trainable market-covered events enough that walk-forward model-family experiments can score at least 30 model-eligible events while preserving leakage controls.

Suggested tasks:

- Identify additional older UFC FightOdds events before the current 37-event window.
- Import and entity-resolve those events into `historical_odds_events`, `historical_odds_fights`, `historical_moneyline_odds`, and `unmatched_historical_odds`.
- Rerun coverage, leakage, market gate, blend, and model-family reports.
- Only create an activation epic if a candidate beats the no-vig market favorite by at least +2pp with stable coverage and non-degraded probability metrics.
