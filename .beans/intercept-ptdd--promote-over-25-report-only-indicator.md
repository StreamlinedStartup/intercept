---
# intercept-ptdd
title: Promote Over 2.5 report-only indicator
status: completed
type: epic
priority: high
created_at: 2026-05-16T05:20:49Z
updated_at: 2026-05-16T05:45:48Z
---

Promote the locked Over 2.5 prop candidate into the product as a report-only market indicator. Scope: Python inference helper using the frozen candidate, API response shape with prop market consensus and no-write policy, upcoming UI display, verification and agent-browser smoke. No automated betting activation.


## Summary of Changes

- Promoted the locked Over 2.5 prop candidate as a report-only market indicator, not an automated betting recommendation.
- Added a committed frozen logistic artifact for `locked_over_2_5_positive_log_c1_conf58` so API runtime scoring does not retrain inline.
- Attached `over_2_5_indicator` to prediction responses with model probability, no-vig market probability, edge, market pair count, threshold, training sample count, and `report_only` status.
- Surfaced the indicator in `/upcoming` fight cards and compare-sheet model tiles while preserving backfill gates and no prop prediction writes.
- Completed focused verification and agent-browser smoke evidence at `data/smoke/over25-report-indicator-upcoming.png`.
