---
# intercept-8a6n
title: 'O25-C: Publish locked Over 2.5 recommendation'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:04:31Z
updated_at: 2026-05-16T05:14:13Z
parent: intercept-dsmc
blocked_by:
    - intercept-rmju
---

Acceptance criteria:
- [x] Publish a concise pass/fail recommendation artifact for locked Over 2.5.
- [x] Separate validated signal, failed signal, and research-only status clearly.
- [x] Specify the next action: build report-only indicator, collect more data, or discard.

## Summary of Changes

- Published `data/experiments/harness/over-2-5-locked-validation-recommendation.md`.
- Recommended promoting `locked_over_2_5_positive_log_c1_conf58` to a report-only Over 2.5 market indicator.
- Preserved the production safety boundary: no automated betting activation until live forward tracking passes review.
- Specified the next implementation shape: expose model probability, market no-vig probability, edge, candidate flag, and live-tracking status.
