# Market Experiment Harness Recommendation

Use the harness as the fast experiment layer for market-scored model, feature, and blend variants.

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
PYTHONPATH=services/python \
/Users/vulturestudio/intercept/services/python/.venv/bin/python \
  -m ml.experiment_harness \
  --config configs/experiments/market-grid.example.json \
  --stdout summary
```

The first matrix found that `blend_25_availability_75_market` was the best configured candidate, but it still missed the market gate:

| Metric | Delta vs market favorite |
|---|---:|
| ROI | -6.89pp |
| Log loss | 0.0239 worse |
| Brier | 0.0103 worse |

The recommendation stays `research_only`. The harness wrote JSON/Markdown artifacts only and did not write `model_versions`; the count after the run was 14.

## MLflow Posture

MLflow is not needed as the first layer. The immediate bottleneck was not a tracking UI; it was the lack of a reproducible config-driven runner that can execute many variants against the same market baseline. The checked-in config plus JSON/Markdown run registry is easier to review, commit, diff, and reproduce.

Add MLflow later if the registry grows enough that search, comparison dashboards, or artifact browsing become the bottleneck.

## Next Experiment Policy

- Add curated variants through `configs/experiments/*.json`.
- Keep current-corpus runs report-only.
- Promote nothing to validated status until a locked future evaluation slice clears the market gate.

## Verification

- `pytest services/python/test_experiment_harness.py services/python/test_market_signal_experiment.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => 16 passed
- `python -m ml.experiment_harness --config configs/experiments/market-grid.example.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-smoke.json data/experiments/harness/market-grid-summary.json data/experiments/harness/experiment-harness-recommendation.json`
- `select count(*) from model_versions;` => 14

No HTTP/UI smoke gate is required for this epic because it added a pure Python report-only CLI and committed artifacts, not an HTTP endpoint or UI surface.
