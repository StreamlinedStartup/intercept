---
# intercept-x1vw
title: 'D2-C: Round tendency vertical slice'
status: completed
type: task
priority: high
created_at: 2026-05-11T13:30:54Z
updated_at: 2026-05-11T13:40:13Z
parent: intercept-7c3e
blocked_by:
    - intercept-86xa
---

Acceptance criteria:
- [x] Add point-in-time ML features from fight_round_stats for round tendency.
- [x] Include decision_signals.round_tendency in prediction output.
- [x] Add a compare-sheet signal tile for round tendency.
- [x] Add focused Python/API/UI coverage as appropriate.
- [x] Update this bean with verification evidence before completion.


## Summary of Changes
- Added round-tendency model features from point-in-time fight_round_stats and fight result metadata.
- Added decision_signals.round_tendency to Python prediction output and API response typing.
- Added a round-tendency signal tile to the /upcoming compare sheet.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q -x
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- src/routes/predict.test.ts
- services/python/.venv/bin/python -m pytest services/python/test_worker.py -q
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- pnpm biome check --write apps/api/src/routes/predict.ts 'apps/web/src/app/(dashboard)/upcoming/compare-sheet.tsx'

## Note
- The live model artifact must be retrained in D2-E because FEATURE_NAMES now includes the new round-tendency fields.
