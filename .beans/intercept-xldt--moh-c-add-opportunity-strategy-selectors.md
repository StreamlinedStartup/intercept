---
# intercept-xldt
title: 'MOH-C: Add opportunity strategy selectors'
status: completed
type: task
priority: high
created_at: 2026-05-15T16:24:41Z
updated_at: 2026-05-15T16:30:45Z
parent: intercept-77c6
blocked_by:
    - intercept-exy7
---

Acceptance criteria:
- [x] Add selectors for overpriced favorite, undervalued underdog, decision edge, finish edge, and abstain/pass.
- [x] Score each selector against the correct target and market baseline.
- [x] Report selected-fight market baseline for fair ROI/probability comparison.
- [x] Add tests for selector behavior on synthetic predictions.

## Summary of Changes
- Added selection policies for overpriced favorites, undervalued underdogs, decision edges, finish edges, and abstain/pass rows.
- Extended the experiment schema to allow the new opportunity selector types.
- Kept selected-fight winner baselines available for market-comparable selectors and left non-winner targets marked as prop-market unavailable.
- Added synthetic selector tests covering all new policies.
