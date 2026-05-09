---
# intercept-bgxt
title: '1-J: Phase 1 verification + close epic'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T22:10:33Z
parent: intercept-1shv
blocked_by:
    - intercept-ftr2
    - intercept-t04p
---

Verification per docs/ufc-fight-predictor-plan.md#phase-1.

- [x] /upcoming backfill state badges are implemented; initial color depends on the live DB state
- [x] Load Khamzat path verified through the async backfill job
- [x] DB has his fight_results
- [x] Decrement history_count_at_backfill -> stale_count -> Update job -> current
- [x] All three seed endpoints work and return resumable async jobs where needed
- [x] biome + typecheck + vitest green
- [x] Hand off to 1-Sm smoke gate (epic stays open until that passes)

## Summary of Changes

Verified the Phase 1 backfill slice end to end against the live local DB and API.
Khamzat Chimaev already had a current backfill row, so the pristine "all red"
initial state no longer applies in this workspace; verification was adjusted to
use actual DB state and to prove the stale/update transition directly.

Evidence:

- `pnpm biome check .` passed with one existing warning in `apps/web/src/lib/url-state.ts`.
- `pnpm typecheck` passed across all packages.
- `pnpm test` passed: 9 files, 81 tests.
- `SELECT count(*) FROM fight_results WHERE fighter_id='767755fd74662dbf'` returned 10.
- `UPDATE fighter_backfill_state SET history_count_at_backfill=9 WHERE fighter_id='767755fd74662dbf'` made `GET /api/predict/backfill/state/767755fd74662dbf` return `status: "stale_count"` and `new_fight_count: 1`.
- `POST /api/predict/backfill/fighter/767755fd74662dbf` returned an async job, and polling completed with `status: "completed"`.
- The final DB row for Khamzat returned to `status='current'` and `history_count_at_backfill=10`.
- `POST /api/predict/backfill/seed?scope=in-window` returned 202 with `event_count: 3`, `fighter_count: 76`, `queued_count: 76`.
- `POST /api/predict/backfill/seed?scope=ppvs-5y` returned 202 with an `in_progress` `seed:ppvs-5y` job.
- `POST /api/predict/backfill/seed?scope=ufc-5y` returned 202 with an `in_progress` `seed:ufc-5y` job.
