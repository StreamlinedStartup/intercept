---
# intercept-p6v3
title: 'D2-MCU-D: Close remaining scored-event coverage gap'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:33:37Z
updated_at: 2026-05-12T03:48:15Z
parent: intercept-p6uo
blocked_by:
    - intercept-0asz
---

Acceptance criteria:
- [x] Run coverage reporting after the completion batch.
- [x] If scored market-covered events remain below 30, use deterministic review/rematch tooling to address event/fight misses or select a small supplemental candidate set.
- [x] Preserve unresolved rows with explicit reasons rather than dropping them.
- [x] End with either >=30 scored market-covered events or a reportable blocker explaining why the threshold cannot be reached from available data.

Constraints:
- No model tuning in this task.
- No active model_versions writes.

## Summary of Changes

- Added deterministic event alias normalization for `UFC on ESPN <n>`, `UFC on ABC <n>`, numbered Fight Night events, and the `Spivak`/`Spivac` headline spelling difference.
- Reran all-event matching and closed the source-event coverage gap: 37/37 historical odds events now match canonical UFC events.
- Published gap-closed coverage artifacts with explicit unresolved fight-level reasons.

## Verification

- `pnpm --filter @interceptor/db test -- match-historical-odds`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --output data/experiments/market-coverage-unlock-gap-closed-coverage.json --markdown data/experiments/market-coverage-unlock-gap-closed-coverage.md`
- `pnpm --filter @interceptor/db typecheck`
- `jq empty data/experiments/market-coverage-unlock-gap-closed-coverage.json`
