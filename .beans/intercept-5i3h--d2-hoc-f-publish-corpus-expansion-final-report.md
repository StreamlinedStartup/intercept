---
# intercept-5i3h
title: 'D2-HOC-F: Publish corpus expansion final report'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:49Z
updated_at: 2026-05-12T03:17:05Z
parent: intercept-vgy0
blocked_by:
    - intercept-f8c1
---

Acceptance criteria:
- [x] Publish final JSON and Markdown report with match rates and remaining blockers.
- [x] State whether model-improvement work is unblocked.
- [x] Keep conclusions research-only unless the validation gate truly passes.

## Summary of Changes

- Added a repeatable final-report generator for the D2-HOC corpus expansion evidence bundle.
- Published `data/experiments/historical-odds-corpus-expansion-final-report.{json,md}` with coverage, review reasons, leakage audit, baseline, and market-gate results.
- Reported `value_status: insufficient_coverage` and kept model-improvement/value claims blocked because coverage reached 235 fights but only 26/30 scored market-covered events.

## Verification

- `pnpm --filter @interceptor/db report:fightodds:final`
- `jq empty data/experiments/historical-odds-corpus-expansion-final-report.json`
- `pnpm --filter @interceptor/db typecheck`
