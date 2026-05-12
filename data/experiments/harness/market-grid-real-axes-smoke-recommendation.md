# Real-Axis Harness Smoke Recommendation

The real-axis smoke sweep ran successfully and did not find a candidate that clears the market gate.

Best candidate: `logistic_c_025_temperature_150_blend_10`

| Metric | Delta vs market favorite |
|---|---:|
| ROI | -3.65pp |
| Log loss | 0.0075 worse |
| Brier | 0.0031 worse |

The result stays `research_only`.

## Recommendation

Expand real axes, not blend-only sweeps. The smoke run proves the harness can now evaluate hyperparameters, feature subsets, deterministic calibration, and market blends while caching shared base walk-forward predictions.

The next useful sweep should vary:

- XGBoost depth, estimator count, learning rate, and sampling params
- logistic `C`
- feature-group ablations and core-feature subsets
- temperature calibration settings
- a small number of market blends

Do not promote any candidate unless it clears the predeclared market gate on a locked future evaluation slice.

## Verification

- `python -m ml.experiment_harness --config configs/experiments/market-grid-real-axes-smoke.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-real-axes-smoke.json data/experiments/harness/market-grid-real-axes-smoke-recommendation.json`
- `select count(*) from model_versions;` => 14

No HTTP/UI smoke gate is required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
