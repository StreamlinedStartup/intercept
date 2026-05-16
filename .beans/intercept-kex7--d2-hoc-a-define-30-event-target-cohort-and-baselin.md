---
# intercept-kex7
title: 'D2-HOC-A: Define 30-event target cohort and baseline coverage report'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:28Z
updated_at: 2026-05-12T02:32:04Z
parent: intercept-vgy0
---

Acceptance criteria:
- [x] Choose and document the 30-event UFC target window.
- [x] Produce a report-only baseline coverage artifact for the target cohort.
- [x] Confirm the tooling writes no active model_versions.
- [x] Record verification evidence in the bean before completion.



## Summary of Changes
- Defined the D2-HOC target cohort as the first 30 UFC FightOdds events from 2023-01-01 through UFC 299 using the existing range importer selection rules.
- Extended historical odds coverage reporting with a `--target-cohort d2-hoc-30-event` report-only baseline artifact.
- Generated `data/experiments/historical-odds-target-cohort-baseline.{json,md}` showing 3/30 target events currently imported and `writes_model_versions: false`.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
