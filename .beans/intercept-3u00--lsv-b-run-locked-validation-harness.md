---
# intercept-3u00
title: 'LSV-B: Run locked validation harness'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:30:44Z
updated_at: 2026-05-16T02:35:21Z
parent: intercept-j1w3
blocked_by:
    - intercept-vuen
---

Acceptance criteria:
- [x] Run the locked validation config against current corpus.
- [x] Publish JSON/Markdown artifacts.
- [x] Identify whether market-strength and decision-market indicators survive the locked slice.
- [x] Keep findings research-only.

## Summary of Changes

- Ran `prop-signal-locked-validation-v1` against a 20-event locked chronological holdout.
- Published JSON and Markdown artifacts under `data/experiments/harness/`.
- Found raw model candidates still fail the market gate, but inverted market-strength diagnostics survive: market side +45.1% ROI on 20 model-underdog disagreement rows and +17.2% ROI on 84 favorite-warning rows.
- Confirmed finish/inside-distance remains negative on the locked slice and should not be promoted.
