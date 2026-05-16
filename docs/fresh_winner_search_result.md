# Fresh Winner Search Result

The fresh post-holdout variation search found no market-gate-clearing winners.

## Search

- Config: `configs/experiments/fresh-winner-search-v1.json`
- Variants: 7,777
- Fresh slice: imported FightOdds UFC events after `2024-03-09`
- Date range scored: `2025-08-16` to `2026-05-09`
- Model-eligible events: 30
- Model-eligible fights: 304
- Value status: `research_only`
- Writes `model_versions`: `false`

The grid covered the existing selected-fight logistic search route:

- Feature sets: `production_plus_market_context`, `production_plus_all_research_market_context`
- `C`: `0.1`, `0.25`, `0.5`, `1.0`, `1.5`, `2.0`, `2.5`, `3.0`, `5.0`
- Temperature: `1.4`, `1.6`, `1.8`, `2.0`, `2.2`, `2.4`, `2.6`, `3.0`
- Market blend: `0.35`, `0.4`, `0.45`, `0.5`, `0.55`, `0.6`
- Minimum confidence: `0.58` through `0.66`

## Result

- Gate-clearing variants: 0
- Best variant: `log_marketctx_c5p0_temp1p6_blend60_min_confidence0p65`
- Best ROI delta vs selected-market baseline: `+1.48pp`
- Best log-loss delta vs selected-market baseline: `+0.0107`
- Best Brier delta vs selected-market baseline: `+0.0039`

## Interpretation

The best fresh-search variant came close on ROI but still missed the required
`+2pp` ROI gate and had worse probability quality than market. This reinforces
the locked result: the current model route is not validated against the market.

Next research should add genuinely new signal or improve entity/line quality,
not keep tuning blend/confidence knobs over the same feature families.
