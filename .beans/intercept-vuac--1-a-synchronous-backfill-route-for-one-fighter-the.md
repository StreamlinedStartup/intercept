---
# intercept-vuac
title: '1-A: Synchronous backfill route for one fighter (THE SLICE)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T20:11:28Z
parent: intercept-1shv
blocked_by:
    - intercept-o6xw
---

Smallest possible end-to-end: hit a route, fighter is in DB. No worker, no async, no UI yet. Just prove the data path.

- [x] apps/api/src/routes/backfill.ts with POST /api/predict/backfill/fighter/:id
- [x] Route fetches /api/ufcstats/fighter/:id (cached), upserts events/fighters/fights/fight_results/fight_round_stats. Walks history[]; for each fight, fetches /fight/:id and inserts. Synchronous — returns when done.
- [x] After call: SELECT count(*) FROM fight_results WHERE fighter_id='767755fd74662dbf' returns ~10 rows
- [x] No UI changes yet


## Summary of Changes

Added synchronous POST /api/predict/backfill/fighter/:id, wired it into the API, and verified it against fighter 767755fd74662dbf. The route fetched cached fighter data plus fight detail pages, upserted fighter/event/fight/result/round stat rows, and left the UI untouched.

Verification:
- pnpm --filter @interceptor/api typecheck
- curl -X POST http://localhost:3001/api/predict/backfill/fighter/767755fd74662dbf returned status current with inserted fight/result/round counts
- SELECT count(*) FROM fight_results WHERE fighter_id='767755fd74662dbf' returned 10
