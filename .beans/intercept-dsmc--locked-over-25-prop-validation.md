---
# intercept-dsmc
title: Locked Over 2.5 prop validation
status: completed
type: epic
priority: high
created_at: 2026-05-16T05:04:13Z
updated_at: 2026-05-16T05:15:38Z
---

Validate the frozen over_2_5 positive target edge candidate from method-round-prop-targets-v1 on a locked chronological holdout. Scope: freeze config, run report-only harness, publish pass/fail recommendation, verify no production writes, PR closeout. Candidate must remain report-only unless locked validation clears ROI and probability-quality gates.

## Summary of Changes

- Froze the exact Over 2.5 candidate from `method-round-prop-targets-v1`: target `over_2_5`, threshold `0.58`, `positive_target_edge`, logistic regression `C=1.0`, and temperature `1.6`.
- Ran the locked validation on a last-35-event chronological holdout with 358 model-eligible fights and 88.3% Over 2.5 market coverage.
- The candidate cleared the configured market gate: +21.9% ROI delta vs market, -0.0363 log-loss delta, -0.0184 Brier delta, 229 selected rows, and no rejection reasons.
- Published the recommendation to promote this as a report-only Over 2.5 market indicator while preserving the live-forward tracking requirement before production betting activation.
