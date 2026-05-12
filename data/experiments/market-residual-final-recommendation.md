# Market Residual Final Recommendation

- Generated: `2026-05-12T06:05:00Z`
- Epic: `intercept-b6yf`
- Task: `intercept-jnqm`
- Value status: `research_only`
- Writes `model_versions`: `false`

## Decision

Do not promote the feature-availability signal or activate validated/value status. Keep the product research-only.

## Evidence

| Gate | Result |
|---|---|
| Leakage audit | pass, 14/14 checks |
| Market gate | fail; model pick ROI -11.2% vs market favorite 20.0%; required candidate ROI 22.0% |
| Blend gate | fail; best blend `blend_25_model_75_market` ROI 18.5%, -1.5pp vs market |
| Model-family gate | fail; best candidate `blend_25_xgboost_75_market` ROI 10.5%, -8.0pp vs market; log loss and Brier worse than market |
| Signal experiment | fail; `xgboost_feature_availability` ROI -5.5%, -23.9pp vs market |

## Signal Result

| Strategy | Accuracy | Log loss | Brier | ROI |
|---|---:|---:|---:|---:|
| `market_favorite` | 74.7% | 0.5766 | 0.1952 | 18.5% |
| `xgboost_current` | 52.0% | 0.7266 | 0.2641 | -8.9% |
| `xgboost_feature_availability` | 53.8% | 0.7291 | 0.2653 | -5.5% |

The signal improved ROI by +3.5pp and accuracy by +1.8pp versus current XGBoost, but worsened log loss and Brier. It remains -23.9pp ROI versus market favorite, so it does not clear the report-only validation threshold.

## Blockers

- Market favorite remains stronger than current model, blends, model-family candidates, and the feature-availability signal on ROI and probability-quality metrics.
- The feature-availability signal fails Task D minimum validation because it worsens log loss and Brier versus current XGBoost.
- Market-disagreement clusters are market-prior gaps rather than evidence of a missing internal pre-fight feature.

## Artifacts

- `data/experiments/market-residual-final-leakage-audit.json`
- `data/experiments/market-residual-final-buckets.json`
- `data/experiments/market-residual-final-market-gate-report.json`
- `data/experiments/market-residual-final-blend-experiments.json`
- `data/experiments/market-residual-final-model-family-experiments.json`
- `data/experiments/market-signal-experiment.json`

## Next Step

Do not continue tuning feature availability in this epic. Next work should either improve historical market corpus quality/closing-line semantics or define a new pre-fight signal from a source not already encoded in the current feature set.

Keep `value_status` as `research_only`; do not write active `model_versions`.
