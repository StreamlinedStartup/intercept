---
# intercept-fmwf
title: 'O25I-Sm: Browser smoke and PR closeout'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:21:03Z
updated_at: 2026-05-16T05:45:42Z
parent: intercept-ptdd
blocked_by:
    - intercept-sqia
---

Acceptance criteria:
- [x] Run focused Python, API, DB, and UI checks.
- [x] Smoke the upcoming UI with agent-browser and commit screenshot evidence.
- [x] Complete epic summary, open one PR, merge it, and clean up branch/worktree.


## Summary of Changes

- Ran focused Python, API, DB, and web verification after switching Over 2.5 runtime scoring to the frozen artifact.
- Smoked `/upcoming` with agent-browser and saved `data/smoke/over25-report-indicator-upcoming.png`.
- Verified `GET /api/predict/fight/b5299e5b946015e5` returns `over_2_5_indicator` with candidate true, 71.7% model probability, 62.3% market probability, +9.4% edge, 18 market pairs, and `report_only` status.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=/tmp/interceptor-worktrees/promote-over25-report-indicator/services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest /tmp/interceptor-worktrees/promote-over25-report-indicator/services/python/test_prop_indicators.py /tmp/interceptor-worktrees/promote-over25-report-indicator/services/python/test_worker.py /tmp/interceptor-worktrees/promote-over25-report-indicator/services/python/test_experiment_harness.py -q` -> 60 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- --runInBand apps/api/src/routes/predict.test.ts` -> 21 passed.
- `pnpm --filter @interceptor/web test -- --runInBand` -> 4 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api typecheck`; `pnpm --filter @interceptor/web typecheck`; `pnpm --filter @interceptor/db typecheck`; `pnpm biome check .`.
- `agent-browser open http://localhost:3000/upcoming`; `agent-browser snapshot`; `agent-browser screenshot /private/tmp/interceptor-worktrees/promote-over25-report-indicator/data/smoke/over25-report-indicator-upcoming.png`.
