---
# intercept-59vv
title: 'HPO-C: Import one event decision and finish prop slice'
status: completed
type: task
priority: high
created_at: 2026-05-15T23:18:56Z
updated_at: 2026-05-16T00:30:38Z
parent: intercept-1xpw
blocked_by:
    - intercept-6us4
---

Acceptance criteria:
- [x] Extend the FightOdds importer to optionally import decision/finish prop markets for one event.
- [x] Upsert prop rows idempotently with explicit counts and skipped-market reasons.
- [x] Do not alter existing moneyline import semantics.
- [x] Add focused importer tests or dry-run evidence.

## Summary of Changes

- Added optional `--include-props` support to the FightOdds importer for the two-way `DISTANCE` market only.
- Preserved existing moneyline import defaults while reporting prop line counts, skipped prop line counts, imported markets, and skipped market reasons.
- Verified event `5362` imports idempotently with 294 prop rows across 12 distance markets.
