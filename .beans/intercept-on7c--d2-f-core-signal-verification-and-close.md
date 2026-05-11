---
# intercept-on7c
title: 'D2-F: Core signal verification and close'
status: completed
type: task
priority: high
created_at: 2026-05-11T13:31:06Z
updated_at: 2026-05-11T14:06:33Z
parent: intercept-7c3e
blocked_by:
    - intercept-ndr8
---

Acceptance criteria:
- [x] Run focused verification for the core signal epic.
- [x] Complete child bean summaries.
- [x] Keep the core signal epic open until all child tasks, including smoke, are committed.
- [x] Update this bean with verification evidence before completion.


## Summary of Changes
- Ran focused verification across the D2 core signal Python, API, and web surfaces.
- Confirmed Beans graph integrity.
- Left the epic open because D2-Sm smoke gate remains the final child task.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q
- services/python/.venv/bin/python -m pytest services/python/test_worker.py -q
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- src/routes/predict.test.ts
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- pnpm biome check --write apps/api/src/routes/predict.ts apps/api/src/routes/predict.test.ts 'apps/web/src/app/(dashboard)/upcoming/compare-sheet.tsx'
- beans check
