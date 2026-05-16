# Expanded Market Sweep Recommendation

The 103-variant sweep did not find a candidate that clears the market gate.

The best configured candidate was `xgb_prod_blend_01_model_99_market`, a 1% model / 99% market blend:

| Metric | Delta vs market favorite |
|---|---:|
| ROI | 0.00pp |
| Log loss | 0.0008 worse |
| Brier | 0.0003 worse |

The result stays `research_only`. It matched market ROI only because it stayed almost entirely on market probability, and it still worsened probability quality.

## Recommendation

Do not keep adding more blend weights under the current harness axes. Denser weights would mostly search closer to pure market. The next useful work is to make the harness support real new axes:

- Cache base walk-forward predictions so blend sweeps do not retrain identical models repeatedly.
- Add model hyperparameters.
- Add feature subsets and ablations.
- Add calibration variants.
- Add new pre-fight signal candidates from residual analysis.

MLflow is still optional. The bottleneck exposed by this run is not tracking UI; it is experiment-axis depth and repeated retraining.

## Verification

- `python -m ml.experiment_harness --config configs/experiments/market-grid-expanded-100.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-expanded-100.json data/experiments/harness/market-grid-expanded-100-recommendation.json`
- `rg -n "xgb_prod_blend_01_model_99_market|research_only|more_blend_weights_justified|model_versions|No HTTP/UI smoke gate" data/experiments/harness/market-grid-expanded-100-recommendation.*`
- `select count(*) from model_versions;` => 14

No HTTP/UI smoke gate is required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
