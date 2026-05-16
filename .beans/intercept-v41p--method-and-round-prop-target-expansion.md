---
# intercept-v41p
title: Method and round prop target expansion
status: completed
type: epic
priority: high
created_at: 2026-05-16T02:46:21Z
updated_at: 2026-05-16T04:53:27Z
---

Build report-only targets and market baselines for goes-to-decision, finish likelihood, KO/TKO, submission, and over/under rounds. Scope: import/source mapping, target labels/prop market consensus, harness config/artifacts, recommendation, verification/PR. Do not activate betting recommendations or write model_versions.

## Summary of Changes

- Documented prop source shapes for `DISTANCE`, fight-level KO/TKO/submission method metadata, and `OVERUNDER_0.5` through `OVERUNDER_4.5`.
- Extended the importer and experiment harness to support report-only labels, prop consensus, coverage reporting, and positive target edge selection for decision, finish, KO/TKO, submission, and over/under round targets.
- Published `method-round-prop-targets-v1` harness artifacts and a recommendation artifact.
- Found one working discovery candidate: `over_2_5_positive_log_c1_conf58`; it cleared the discovery market gate and should move to locked validation, not production activation.
- Kept decision as a possible market-strength warning, rejected finish/KO/TKO/submission/over 1.5 for current model-edge use, and marked over 3.5/4.5 as coverage-blocked.
