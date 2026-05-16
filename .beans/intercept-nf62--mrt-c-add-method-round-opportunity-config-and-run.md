---
# intercept-nf62
title: 'MRT-C: Add method-round opportunity config and run'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:46:34Z
updated_at: 2026-05-16T04:50:41Z
parent: intercept-v41p
blocked_by:
    - intercept-j4xo
---

Acceptance criteria:
- [x] Add report-only harness config covering goes-to-decision, finish, KO/TKO, submission, and over/under rounds where supported.
- [x] Run the harness and publish JSON/Markdown artifacts.
- [x] Report which targets have market-backed ROI and which are coverage-blocked.

## Summary of Changes

- Added `configs/experiments/method-round-prop-targets-v1.json` as a report-only discovery matrix for decision, finish, KO/TKO, submission, and over 1.5/2.5/3.5/4.5.
- Ran the harness and published JSON/Markdown artifacts under `data/experiments/harness/method-round-prop-targets-v1.*`.
- Found one discovery candidate: `over_2_5_positive_log_c1_conf58` cleared the market gate with +21.9% ROI delta, -0.0024 log-loss delta, and -0.0057 Brier delta versus market. This is not activation proof and requires locked future-slice validation.
- Decision, finish, KO/TKO, submission, over 1.5, over 3.5, and over 4.5 remained report-only rejects; over 3.5/4.5 are especially coverage-limited at roughly 4% market-backed coverage.
