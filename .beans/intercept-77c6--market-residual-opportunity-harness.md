---
# intercept-77c6
title: Market residual opportunity harness
status: completed
type: epic
priority: high
created_at: 2026-05-15T16:24:22Z
updated_at: 2026-05-15T17:44:21Z
parent: intercept-8mw9
---

Build an efficient report-only harness for betting-opportunity experiments that use the market as baseline. Scope includes multi-target labels, strategy-specific residual scoring, cached model/prediction reuse, and JSON/Markdown reports for promote/iterate/reject decisions.

## Summary of Changes
- Extended the config-driven market harness with explicit `winner`, `decision`, and `finish` targets.
- Added decision/finish labels, target-aware metrics, and opportunity selectors for overpriced favorites, undervalued underdogs, decision edge, finish edge, and abstain/pass rows.
- Added smoke and focused opportunity matrices that reuse cached base predictions across selector, threshold, calibration, and blend variants.
- Published report-only evidence under `data/experiments/harness`; no candidate cleared the market gate, and decision/finish market validation remains blocked on historical prop odds.
