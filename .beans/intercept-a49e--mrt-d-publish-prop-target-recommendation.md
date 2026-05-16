---
# intercept-a49e
title: 'MRT-D: Publish prop target recommendation'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:46:38Z
updated_at: 2026-05-16T04:52:07Z
parent: intercept-v41p
blocked_by:
    - intercept-nf62
---

Acceptance criteria:
- [x] Publish a concise recommendation artifact for decision, finish, KO/TKO, submission, and rounds.
- [x] Separate working market indicators from unsupported or failed targets.
- [x] Specify the next data/import action for any blocked target.

## Summary of Changes

- Published `data/experiments/harness/method-round-prop-target-recommendation.md`.
- Promoted only `over_2_5_positive_log_c1_conf58` to locked validation, with explicit report-only status and no production activation.
- Classified decision as a possible market-strength warning, rejected finish/KO/TKO/submission/over 1.5 for current model-edge use, and marked over 3.5/4.5 as coverage-blocked despite high simulated ROI.
- Documented the next data actions: preserve `DISTANCE` and `OVERUNDER_*`, keep fight-level method metadata, avoid sparse single-sided fighter props, and expand over 3.5/4.5 coverage before interpreting those targets.
