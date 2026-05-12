---
# intercept-ftbt
title: 'D2-TMC: Trainable market-covered corpus expansion'
status: completed
type: epic
priority: high
created_at: 2026-05-12T04:23:27Z
updated_at: 2026-05-12T04:42:59Z
parent: intercept-8mw9
---

Expand the historical odds corpus backward enough that walk-forward model-family experiments can score at least 30 model-eligible market-covered UFC events. Keep all outputs research-only; no active model_versions writes or validated activation in this epic.

Acceptance criteria:
- [x] Define the additional older UFC FightOdds target window needed to raise model-eligible events above 30.
- [x] Import and entity-resolve the target window into historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [x] Rerun leakage, coverage, market gate, blend, and model-family reports against the expanded corpus.
- [x] Publish a final JSON/Markdown decision report with model-eligible event count, candidate ROI deltas, remaining blockers, and next recommendation.
- [x] Keep UI/API/docs research-only and do not write active model_versions.

## Summary of Changes

- Expanded FightOdds coverage from 37 to 51 matched source events by importing and resolving a 14-event older UFC target window.
- Improved event matching with a deterministic participant-overlap fallback for changed FightOdds headlines.
- Increased trainable market-covered model-family evaluation from 26 to 40 model-eligible events.
- Published D2-TMC coverage, leakage, market gate, blend, model-family, and final decision artifacts.
- Final status remains `research_only`: trainability is unblocked, but validated activation is still blocked because candidates trail the no-vig market favorite.

## Verification

- `./scripts/ci-local.sh`
- `jq empty data/experiments/trainable-market-corpus-final-report.json`
