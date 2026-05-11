---
# intercept-c483
title: 'D2-D: Common opponent vertical slice'
status: completed
type: task
priority: high
created_at: 2026-05-11T13:30:58Z
updated_at: 2026-05-11T13:43:02Z
parent: intercept-7c3e
blocked_by:
    - intercept-x1vw
---

Acceptance criteria:
- [x] Add point-in-time shared-opponent metrics.
- [x] Include decision_signals.common_opponents in prediction output.
- [x] Add a compare-sheet signal tile for common opponents.
- [x] Test shared opponents, no shared opponents, and future-data exclusion.
- [x] Update this bean with verification evidence before completion.


## Summary of Changes
- Added point-in-time common-opponent feature metrics for shared opponent count and win differential.
- Added decision_signals.common_opponents to prediction outputs and API typing.
- Added a common-opponents signal tile to the /upcoming compare sheet.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q -x
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- src/routes/predict.test.ts
- services/python/.venv/bin/python -m pytest services/python/test_worker.py -q
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- pnpm biome check --write apps/api/src/routes/predict.ts 'apps/web/src/app/(dashboard)/upcoming/compare-sheet.tsx'

## Note
- The live model artifact must be retrained in D2-E because FEATURE_NAMES now includes common-opponent fields.
