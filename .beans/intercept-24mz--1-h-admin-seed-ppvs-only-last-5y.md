---
# intercept-24mz
title: '1-H: Admin seed: PPVs only (last 5y)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T22:06:48Z
parent: intercept-1shv
blocked_by:
    - intercept-g6vf
---

Wider seed for training-set bootstrap.

- [x] POST /api/predict/backfill/seed?scope=ppvs-5y
- [x] Walks events/completed?page=N filtering name LIKE 'UFC %' (numbered) AND date>=now-5y
- [x] Same per-fighter pipeline downstream
- [x] Admin button: 'Seed: PPVs (5y)' with progress

## Summary of Changes

Added `scope=ppvs-5y` to the admin seed endpoint. Because this seed can collect dozens of event cards and hundreds of fighters, it now returns immediately with an in-process seed job and performs PPV discovery plus per-fighter backfill in the background. The admin training page now exposes a `Seed: PPVs (5y)` button and polls the existing backfill job endpoint for progress.

Verification:
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check apps/api/src/routes/backfill.ts apps/web/src/app/(dashboard)/admin/predict-train/predict-train-content.tsx`
- `curl -i -sS -X POST 'http://localhost:3001/api/predict/backfill/seed?scope=ppvs-5y'` returned `202` immediately with `scope: "ppvs-5y"` and an `in_progress` seed job.
