---
# intercept-mlyq
title: '1-B: fighter_backfill_state row written + GET state route'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T20:13:50Z
parent: intercept-1shv
blocked_by:
    - intercept-vuac
---

Persist that we backfilled them, expose state via GET.

- [x] After 1-A completes for a fighter, write a fighter_backfill_state row (status='current', history_count_at_backfill, last_known_fight_id, last_backfilled_at)
- [x] GET /api/predict/backfill/state/:fighterId returns that row (or {status: 'none'} if absent)
- [x] Curl test: POST then GET → state='current'

## Summary of Changes

Added GET /api/predict/backfill/state/:fighterId to expose persisted backfill state, including a none-state response for fighters without a row.

Verification:
- pnpm --filter @interceptor/api typecheck
- curl -X POST http://localhost:3001/api/predict/backfill/fighter/767755fd74662dbf returned status current
- curl http://localhost:3001/api/predict/backfill/state/767755fd74662dbf returned status current, history_count_at_backfill=10, last_known_fight_id=12cedec11b37ddc0
- curl http://localhost:3001/api/predict/backfill/state/0000000000000000 returned status none
