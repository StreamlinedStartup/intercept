# Mass Edge Search Recommendation

The en-masse harness works, but the mass search did not find a candidate edge.

- Variants: 1,585
- Cached base keys: 66
- Gate-clearing candidates: 0
- Best candidate: `log_c025_core_stats_temp200_blend01`
- Value status: `research_only`

## Result

The best candidate was a 1% model / 99% market blend.

| Metric | Delta vs market favorite |
|---|---:|
| ROI | 0.00pp |
| Log loss | 0.0006 worse |
| Brier | 0.0002 worse |

That is not an edge. It ties market ROI only by staying almost entirely on market probability, while still degrading probability quality.

## Next Highest-Leverage Work

Do not spend the next cycle adding more variants over the same feature families. The mass harness is now good enough to search quickly; the limiting factor is candidate signal and corpus quality.

The next highest-leverage work is:

- Expand and clean historical odds coverage so candidate selection is less constrained by 40 model-eligible events.
- Generate genuinely new pre-fight signal candidates from residual clusters instead of more variants of the same feature families.
- Add a locked holdout/future slice workflow before considering any candidate promotion.

## Verification

- `python -m ml.experiment_harness --config configs/experiments/market-grid-mass-edge-search.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-mass-edge-search.json data/experiments/harness/market-grid-mass-edge-search-summary.json data/experiments/harness/market-grid-mass-edge-search-recommendation.json`
- `select count(*) from model_versions;` => 14

No HTTP/UI smoke gate is required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
