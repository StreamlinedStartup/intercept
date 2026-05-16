---
# intercept-en2g
title: 'PMB-D: Run prop-baseline opportunity report'
status: completed
type: task
priority: high
created_at: 2026-05-16T00:51:43Z
updated_at: 2026-05-16T01:02:54Z
parent: intercept-zh6a
blocked_by:
    - intercept-vpf7
---

Acceptance criteria:
- [x] Run a market opportunity config that includes decision and finish prop-baseline variants.
- [x] Publish JSON/Markdown artifacts under data/experiments/harness.
- [x] State whether any decision/finish variant clears the gate or remains research-only.
- [x] Include no model promotion or betting activation language.

## Summary of Changes

- Ran `market-opportunity-matrix-v1` with prop-backed decision and finish baselines.
- Published updated JSON and Markdown artifacts under `data/experiments/harness/`.
- Confirmed `finish_edge_log_c1_conf62` ranks first but remains research-only and fails the configured market gate.
