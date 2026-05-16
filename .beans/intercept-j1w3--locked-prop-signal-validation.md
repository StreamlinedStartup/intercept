---
# intercept-j1w3
title: Locked prop signal validation
status: completed
type: epic
priority: high
created_at: 2026-05-16T02:30:34Z
updated_at: 2026-05-16T02:38:39Z
---

Validate the research-only market-strength and decision-market indicators from intercept-fmpi on a locked evaluation slice. Scope: locked config, harness output, recommendation update, verification/PR. Do not activate betting recommendations or write model_versions.

## Summary of Changes

- Added and ran `prop-signal-locked-validation-v1` on the latest 20 chronological events.
- Found raw model candidates still fail the market gate, but market-side interpretations of model disagreement held up as research indicators.
- Published the next action: a report-only `market_favorite_strength_warning` alert, with finish/KO proxy deferred until method-specific props are imported.
