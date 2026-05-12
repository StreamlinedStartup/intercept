# Trainable Market-Corpus Final Report

- Generated: `2026-05-12T04:40:01Z`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Trainability status: `unblocked`
- Validated activation unblocked: `false`

## Decision

The corpus expansion cleared the trainable market-covered event floor, but no candidate clears the market-favorite ROI and probability-quality gate. Continue research-only model improvement; do not activate validated status.

## Corpus Delta

| Metric | Before | After |
|---|---:|---:|
| Market-covered events | 37 | 51 |
| Scored fights | 345 | 486 |
| Model-eligible events | 26 | 40 |
| Model-eligible fights | 241 | 379 |

## Gate Results

| Gate | Result |
|---|---|
| Leakage audit | pass, 15/15 checks |
| Coverage | pass, 51 events and 486 fights |
| Market gate | fail, candidate must beat +20.0% market favorite ROI by +2pp |
| Model-family gate | fail, best candidate trails market favorite by 8.0pp |

## Candidate Results

| Candidate | Scope | ROI | Delta vs market | Gate |
|---|---|---:|---:|---|
| market_favorite | full market-covered corpus | 20.0% | baseline | pass baseline |
| model_pick | full market-covered corpus | -11.2% | -31.2pp | fail |
| blend_25_model_75_market | full market-covered corpus | 18.5% | -1.5pp | fail |
| blend_25_xgboost_75_market | model-eligible subset | 10.5% | -8.0pp | fail |

## Remaining Blockers

- The market favorite remains the strongest baseline on ROI, log loss, and Brier score.
- Current pre-fight features and tested model families do not add signal beyond the market.
- Validated/value activation requires a separate activation epic only after a candidate beats market favorite by at least +2pp without probability-quality regression.

## Next Recommended Epic

`D2-MRA: Market residual analysis and pre-fight signal discovery`

Goal: use the now-trainable 40-event market-covered corpus to identify where the model disagrees with the market, which feature gaps explain those misses, and which new pre-fight signals are worth adding before another model-family experiment.

Suggested tasks:

- Bucket model and market errors by weight class, event age, favorite/underdog side, odds range, and feature availability.
- Identify high-loss residual clusters where the model is confidently wrong against the market.
- Audit feature availability for those clusters and define one or two pre-fight-only signal additions.
- Implement the smallest signal addition and rerun the same market-gated reports.
- Keep outputs research-only unless a later activation epic passes the market gate.
