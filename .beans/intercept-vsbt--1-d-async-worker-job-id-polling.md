---
# intercept-vsbt
title: '1-D: Async worker + job_id polling'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T20:28:04Z
parent: intercept-1shv
blocked_by:
    - intercept-g7uh
---

Synchronous routes block the API on long backfills. Move to in-process worker with polling. Refactor 1-A and 1-C to async.

- [x] apps/api/src/services/backfill-worker.ts: Map<jobId, {fighterId, status, progress, error, startedAt}>
- [x] POST /api/predict/backfill/fighter/:id returns {job_id} immediately, status='in_progress'
- [x] GET /api/predict/backfill/job/:job_id returns current state
- [x] UI polls job every 1s while in_progress; show progress text 'Loading fight 3 of 10'
- [x] On completion, refetch backfill state for the fighter (re-renders badge)
- [x] Crash recovery: jobs disappear on api restart; user sees state='in_progress' but no job → treat as failed and re-allow click

## Summary of Changes

Moved fighter backfill execution into an in-process worker map. POST now returns a job immediately, GET /api/predict/backfill/job/:job_id exposes progress, and the UI polls once per second while showing disabled inline progress text.

Verification:
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- curl -X POST http://localhost:3001/api/predict/backfill/fighter/767755fd74662dbf returned status in_progress with job_id
- curl /api/predict/backfill/job/<job_id> returned completed with progress current=9 total=9
- curl /api/predict/backfill/job/not-a-real-job returned 404 with status failed
- agent-browser on /upcoming showed Joshua Van button disabled as Loading fight 2 of 10, then Joshua Van image current after completion
