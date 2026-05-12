---
# intercept-aeef
title: 'D2-RV-D: Expand historical odds match coverage'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:19Z
updated_at: 2026-05-12T01:08:51Z
parent: intercept-dmyw
blocked_by:
    - intercept-tjvc
---

Improve historical odds match coverage before using market comparisons for any validation claim.

Acceptance criteria:
- [ ] Expand canonical matching coverage across more UFC events.
- [x] Keep unmatched rows reviewable instead of silently dropping them.
- [ ] Report coverage by source event, canonical event, fights, and fighter rows.
- [x] Do not write active model_versions.



## Summary of Changes
- Added `match:fightodds:all` so every imported FightOdds event can be matched in one repeatable command without closing the DB connection between events.
- Added `report:fightodds:coverage` to write source-event, canonical-event, fight, moneyline, and review-row coverage artifacts.
- Matched all 3 imported FightOdds events, linking 30/46 fights and 1,553/2,173 moneyline rows while preserving 63 review rows for unmatched/cancelled fights.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --output data/experiments/historical-odds-coverage.json --markdown data/experiments/historical-odds-coverage.md`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
