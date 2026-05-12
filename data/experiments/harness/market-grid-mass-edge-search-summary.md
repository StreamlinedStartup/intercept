# Mass Edge Search Summary

- Variants: 1,585
- Cached base keys: 66
- Model-eligible corpus: 40 events, 379 fights
- Gate-clearing candidates: 0
- Value status: `research_only`
- `model_versions` after run: 14

## Best Candidate

`log_c025_core_stats_temp200_blend01`

| Metric | Delta vs market favorite |
|---|---:|
| ROI | 0.00pp |
| Log loss | 0.0006 worse |
| Brier | 0.0002 worse |

The best candidate is a 1% model / 99% market blend. It ties market ROI only by staying almost entirely on market probability, while still worsening log loss and Brier. The mass search found no candidate edge on the current corpus.

## Verification

- `python -m ml.experiment_harness --config configs/experiments/market-grid-mass-edge-search.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-mass-edge-search.json data/experiments/harness/market-grid-mass-edge-search-summary.json`
- `select count(*) from model_versions;` => 14
