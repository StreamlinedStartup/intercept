---
# intercept-yenm
title: 'SIR-E: Weekly post-event indicator evaluation'
status: todo
type: task
created_at: 2026-05-16T05:58:25Z
updated_at: 2026-05-16T05:58:25Z
parent: intercept-qh8w
blocked_by:
    - intercept-e042
---

Define the weekly post-event evaluation job for report-only indicator quality tracking.

Acceptance criteria:
- [ ] Weekly flow imports completed events/results and refreshes fighter histories after results settle.
- [ ] Target labels are updated for decision, finish, KO/TKO, submission, and Over/Under round thresholds where data supports them.
- [ ] Prior indicator snapshots are compared against actual outcomes without changing production artifacts.
- [ ] Report artifacts summarize hit rate, calibration, coverage, market edge behavior, stale/missing-data rates, and known limitations.
- [ ] Job remains report-only and never activates betting recommendations.
