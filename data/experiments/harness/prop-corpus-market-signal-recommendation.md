# Prop Corpus Market Signal Recommendation

- Generated from: `data/experiments/harness/market-opportunity-matrix-v1.json`
- Corpus: 70 model-eligible events, 683 model-eligible fights
- Status: `research_only`
- Writes `model_versions`: `false`

## Bottom Line

No raw model betting candidate clears the market gate. The useful finding is an indicator layer: when this model disagrees with the moneyline market, the disagreement currently behaves more like a warning that the market is strong than like an invitation to fade the market.

This should become a market-strength filter, not an active bet signal yet.

## Potentially Useful Indicators

| Indicator | Evidence | Read |
|---|---:|---|
| Market too strong against model underdog, blended selector | 40 selected rows; market side +24.6% ROI; +13.1% vs full market favorite baseline | When the model likes an underdog after a 40% market blend, the better research action is currently to respect the market favorite. |
| Market too strong against model underdog, unblended selector | 112 selected rows; market side +20.4% ROI; +8.8% vs full market favorite baseline | The model-supported underdog target is inverted; use it as a possible overconfidence warning against betting the dog. |
| Market favorite holds despite model warning | 271 selected rows; market side +16.7% ROI; +5.2% vs full market favorite baseline | Favorite-underperformance flags are not producing favorite fades; they identify market favorites that still hold up. |
| Decision market strength after model filter | 49 prop-backed rows; selected decision market side +14.8% ROI | Decision/going-the-distance is the first prop area worth locking for future validation. |
| Market side positive when model abstains | 56 rows; selected market side +2.2% ROI | Low model confidence is not enough to pass automatically; market price remains useful. |

## Ruled Out For Now

| Target | Result | Decision |
|---|---|---|
| Finish likelihood / KO potential proxy | Finish/inside-distance candidate is closest in ranking but still negative: model ROI -14.2%, selected prop-market ROI -13.9% across 81 rows | Do not promote finish/KO proxy yet. Import method-specific KO/TKO and submission props before revisiting. |
| Exact winner prediction | Market favorite baseline remains much stronger: +11.5% ROI, 72.8% accuracy, 0.5819 log loss | Keep winner prediction secondary; use model disagreement as a market-strength indicator. |
| Underdog value | Model underdog selections lose badly: -32.4% to -34.7% ROI | Treat as inverted signal until a locked holdout proves otherwise. |
| Favorite fade / overpriced favorite | Model-side fade loses -5.1% ROI while market favorite side is +16.7% | Do not fade favorites from this signal. |

## Next Action

Create a locked future-slice evaluation for two research indicators:

1. `market_too_strong_against_model_underdog`: bet or flag the market side when model-underdog selectors fire.
2. `decision_market_strength_after_model_filter`: evaluate goes-to-decision market-side picks on model-filtered rows.

Activation remains blocked until the locked slice preserves positive ROI without worsening probability quality. The current corpus is discovery evidence only.
