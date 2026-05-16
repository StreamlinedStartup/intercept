---
# intercept-yenm
title: 'SIR-E: Weekly post-event indicator evaluation'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:25Z
updated_at: 2026-05-16T14:15:47Z
parent: intercept-qh8w
blocked_by:
    - intercept-e042
---

Define the weekly post-event evaluation job for report-only indicator quality tracking.

Acceptance criteria:
- [x] Weekly flow imports completed events/results and refreshes fighter histories after results settle.
- [x] Target labels are updated for decision, finish, KO/TKO, submission, and Over/Under round thresholds where data supports them.
- [x] Prior indicator snapshots are compared against actual outcomes without changing production artifacts.
- [x] Report artifacts summarize hit rate, calibration, coverage, market edge behavior, stale/missing-data rates, and known limitations.
- [x] Job remains report-only and never activates betting recommendations.

## Summary of Changes

- Added `ml.evaluate_market_indicators` and `pnpm --filter @interceptor/db report:market-indicators` for report-only post-event indicator evaluation.
- The evaluator derives decision, finish, KO/TKO, submission, and Over/Under labels from resolved fight result method/round data and compares prior snapshots against outcomes.
- The weekly operations doc now covers completed-result import plus JSON/Markdown evaluation artifacts; local verification generated an empty-current-corpus report without writing production artifacts.
