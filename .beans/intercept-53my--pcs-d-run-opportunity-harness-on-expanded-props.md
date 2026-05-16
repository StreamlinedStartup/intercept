---
# intercept-53my
title: 'PCS-D: Run opportunity harness on expanded props'
status: completed
type: task
priority: high
created_at: 2026-05-16T01:13:39Z
updated_at: 2026-05-16T02:18:24Z
parent: intercept-fmpi
blocked_by:
    - intercept-ely2
---

Acceptance criteria:
- [x] Rerun market-opportunity-matrix-v1 against expanded prop coverage.
- [x] Publish updated harness artifacts.
- [x] Identify any potentially market-beating decision/finish/favorite/underdog/abstain indicators.
- [x] Keep output report-only unless a later locked evaluation is explicitly created.

## Summary of Changes

- Reran `market-opportunity-matrix-v1` on the expanded prop corpus and regenerated JSON/Markdown artifacts.
- Added repeatable signal diagnostics to the harness so selected-market ROI is reported for model-filtered subsets.
- Found market-strength indicators: model-underdog disagreement currently favors the market side (+20.4% to +24.6% selected-market ROI), and model-filtered decision rows show +14.8% selected-market ROI.
- Kept all outputs `research_only` with `writes_model_versions=false`; no active betting recommendation was promoted.
