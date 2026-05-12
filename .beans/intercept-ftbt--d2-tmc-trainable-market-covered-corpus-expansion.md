---
# intercept-ftbt
title: 'D2-TMC: Trainable market-covered corpus expansion'
status: todo
type: epic
priority: high
created_at: 2026-05-12T04:23:27Z
updated_at: 2026-05-12T04:23:27Z
parent: intercept-8mw9
---

Expand the historical odds corpus backward enough that walk-forward model-family experiments can score at least 30 model-eligible market-covered UFC events. Keep all outputs research-only; no active model_versions writes or validated activation in this epic.

Acceptance criteria:
- [ ] Define the additional older UFC FightOdds target window needed to raise model-eligible events above 30.
- [ ] Import and entity-resolve the target window into historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [ ] Rerun leakage, coverage, market gate, blend, and model-family reports against the expanded corpus.
- [ ] Publish a final JSON/Markdown decision report with model-eligible event count, candidate ROI deltas, remaining blockers, and next recommendation.
- [ ] Keep UI/API/docs research-only and do not write active model_versions.
