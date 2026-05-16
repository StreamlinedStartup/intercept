---
# intercept-1xpw
title: Historical prop odds source and import
status: completed
type: epic
priority: high
created_at: 2026-05-15T23:18:32Z
updated_at: 2026-05-16T00:46:47Z
parent: intercept-8mw9
---

Discover and import the smallest useful historical FightOdds prop-odds slice for decision and finish market validation. Scope: source shape discovery, prop odds schema/import contract, one-event import, canonical matching/reporting, and research-only harness readiness. Do not activate betting recommendations.

## Summary of Changes

- Discovered FightOdds prop offer shape for event `5362` and confirmed the two-way `DISTANCE` market supports decision/finish baselines.
- Added `historical_prop_odds`, optional `--include-props` import support, and a prop coverage/readiness report.
- Published report-only artifacts showing 294 linked prop rows across 12 distance markets; no betting recommendations or model promotion were activated.
