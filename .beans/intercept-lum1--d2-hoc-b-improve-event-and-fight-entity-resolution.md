---
# intercept-lum1
title: 'D2-HOC-B: Improve event and fight entity-resolution heuristics'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:33Z
updated_at: 2026-05-12T02:39:19Z
parent: intercept-vgy0
blocked_by:
    - intercept-kex7
---

Acceptance criteria:
- [x] Improve matching with normalized names, event date, promotion, weight class, bout participants, and cancelled-bout handling.
- [x] Verify no regression on the current 3-event historical odds corpus.
- [x] Keep unresolved rows reportable instead of silently dropping them.



## Summary of Changes
- Expanded FightOdds/UFCStats participant matching for name particles, transposed given/family names, diacritics, and known source aliases.
- Preserved cancelled source bouts as reviewable unmatched rows instead of linking them to canonical completed fights.
- Included canonical weight class in candidate review rows and cleared stale match-review rows when a fight becomes matched.
- Regenerated historical odds coverage artifacts after rematching the current 3-event corpus.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all` => 37/46 fights matched, 0 ambiguous, 9 unmatched cancelled fights, 1,915 linked moneyline rows.
- `psql postgres://interceptor:interceptor@localhost:5434/interceptor -c "select match_status, is_cancelled, count(*) from historical_odds_fights group by match_status, is_cancelled order by match_status, is_cancelled;"` => 37 matched active fights, 9 unmatched cancelled fights.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
