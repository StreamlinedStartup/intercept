---
# intercept-6us4
title: 'HPO-A: Discover FightOdds prop offer shape'
status: completed
type: task
priority: high
created_at: 2026-05-15T23:18:44Z
updated_at: 2026-05-15T23:22:32Z
parent: intercept-1xpw
---

Acceptance criteria:
- [x] Inspect the current FightOdds event GraphQL shape for prop markets on one matched UFC event.
- [x] Identify whether decision, does-not-go-decision, inside-distance, KO/TKO, and submission markets are present.
- [x] Record exact fields needed for source fight id, prop market id/name, outcomes, sportsbook, odds, and oddsPrev semantics.
- [x] Publish a compact discovery artifact without writing production tables.

## Summary of Changes

- Probed `eventOfferTable(pk: 5362)` and `fightPropOfferTable(slug: "brandon-moreno-vs-brandon-royval-51622")` for a matched UFC event with 76 prop offers.
- Confirmed the two-way `DISTANCE` market supports fight-goes-decision and finish-likelihood targets with sportsbook-level outcome odds.
- Documented the import field contract and first-slice recommendation in `data/experiments/fightodds-prop-shape-discovery.md`.
