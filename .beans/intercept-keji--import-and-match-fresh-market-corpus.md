---
# intercept-keji
title: Import and match fresh market corpus
status: completed
type: task
priority: high
created_at: 2026-05-13T00:57:17Z
updated_at: 2026-05-13T01:06:04Z
parent: intercept-tco0
blocked_by:
    - intercept-jk96
---

Acceptance criteria:
- [x] Import UFC FightOdds events after 2024-03-09 when available.
- [x] Run historical odds matcher on imported rows.
- [x] Generate fresh coverage evidence or document source blocker.
- [x] Keep all outputs report-only.



## Summary of Changes

- Imported 30 post-holdout UFC FightOdds events by explicit sitemap-derived PK after range pagination returned HTTP 429.
- Matched the expanded corpus with the existing historical odds matcher.
- Added fresh import and coverage artifacts under data/experiments.

## Verification

- import:fightodds:event imported 30 events, 438 fights, and 35,046 moneyline rows with 0 failed events.
- match:fightodds:all linked the combined corpus to 809 matched fights and 54,298 moneyline rows.
- report:fightodds:coverage generated data/experiments/fresh-market-coverage.{json,md}.
- Fresh post-2024-03-09 SQL summary: 30 events, 438 source fights, 310 matched fights, 26,260 linked moneyline rows.
