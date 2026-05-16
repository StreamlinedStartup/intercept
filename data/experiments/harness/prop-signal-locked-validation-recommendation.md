# Locked Prop Signal Validation Recommendation

- Source report: `data/experiments/harness/prop-signal-locked-validation-v1.json`
- Holdout: latest 20 chronological events, 206 fights
- Holdout dates: `2025-11-08` through `2026-05-09`
- Status: `research_only`
- Writes `model_versions`: `false`

## Decision

Do not promote any raw model betting pick. Every configured model candidate failed the market gate on ROI delta, log loss, Brier score, and coverage stability.

The useful signal is the inverted market-strength read: when the model argues with the market, the market side still performs better. This survived the locked holdout strongly enough to keep testing as a filter or alert.

## Held Up

| Signal | Locked result | Recommendation |
|---|---:|---|
| Model-underdog disagreement as market-strength warning | 20 selected rows; market side +45.1% ROI; 85.0% accuracy; +34.6% ROI delta vs full market baseline | Keep. Build as a research indicator that says the market favorite may be stronger than the model thinks. |
| Favorite-warning rows still favor market side | 84 selected rows; market side +17.2% ROI; 82.1% accuracy; +6.7% ROI delta vs full market baseline | Keep. Treat favorite-underperformance flags as “do not fade favorite yet” warnings. |
| Blended underdog disagreement | 3 selected rows; market side +70.7% ROI; 100.0% accuracy | Promising but too small. Keep only as supporting evidence, not as a standalone rule. |

## Weakened

| Signal | Locked result | Recommendation |
|---|---:|---|
| Decision market strength after model filter | 26 selected rows; selected decision-market ROI +10.7%; +0.3% ROI delta vs full market baseline | Keep watching, but this did not materially beat the broader market baseline on the locked slice. Needs more prop coverage or stricter filtering. |

## Failed

| Signal | Locked result | Recommendation |
|---|---:|---|
| Finish / KO-potential proxy | 53 selected rows; model ROI -26.0%; selected prop-market ROI -18.4% | Stop testing this as a DISTANCE-only proxy. Import method-specific KO/TKO and submission props before testing KO potential again. |
| Raw model underdog value | Model ROI -58.5% to -100.0% | Treat as inverted signal only. Do not bet model-selected dogs. |
| Raw favorite fade | Model-side ROI -7.5% | Do not fade market favorites from this model signal. |

## Next Implementation Slice

Add a report-only “market-strength alert” output that materializes the held-up indicator per fight:

- Trigger when the model selects the underdog against the market with at least 0.05 model-vs-market edge.
- Alert should say: `market_favorite_strength_warning`.
- Include market favorite, model dog, market probability, model probability, edge, and whether the row is inside a locked-validation-supported rule.
- Keep it out of production betting recommendations until another future holdout preserves the signal.

This gives us a working market indicator without pretending the winner model beats the market.
