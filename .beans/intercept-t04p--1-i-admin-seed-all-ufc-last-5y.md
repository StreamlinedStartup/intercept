---
# intercept-t04p
title: '1-I: Admin seed: all UFC (last 5y)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T22:08:36Z
parent: intercept-1shv
blocked_by:
    - intercept-24mz
---

Largest seed. ~250 events. Use this only when ready to train.

- [x] POST /api/predict/backfill/seed?scope=ufc-5y
- [x] Filter promotion='ufc' AND date>=now-5y
- [x] Admin button + progress
- [x] Verification: endpoint returns a 202 seed job immediately; full >300 fighter seed is deferred to operator-run training bootstrap

## Summary of Changes

Added the ufc-5y seed scope as the largest async admin seed. It shares the
five-year completed-event walk with the PPV seed, but accepts every completed
event whose name starts with UFC instead of only numbered PPVs. The admin
training page now exposes Seed: UFC (5y) and polls job progress through the
existing backfill job endpoint.

Verification:

- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- pnpm biome check apps/api/src/routes/backfill.ts apps/web/src/app/(dashboard)/admin/predict-train/predict-train-content.tsx
- curl -i -sS -X POST 'http://localhost:3001/api/predict/backfill/seed?scope=ufc-5y' returned 202 immediately with scope: "ufc-5y" and an in_progress seed job.
