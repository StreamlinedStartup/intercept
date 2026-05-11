---
# intercept-vxdl
title: Contextual intelligence overlay
status: completed
type: epic
priority: normal
created_at: 2026-05-11T13:30:42Z
updated_at: 2026-05-11T19:20:06Z
parent: intercept-8mw9
blocked_by:
    - intercept-qizd
---

Epic 3 for Decision Engine v2. Define and ship a separate auditable overlay for injury, camp, weight-cut, and short-notice context. Keep it out of model-training features until labels and backtests exist.

## Summary of Changes

- Completed the contextual overlay ontology in `docs/contextual_overlay_ontology.md`.
- Linked the ontology from `docs/decision_engine_v2.md`.
- Kept contextual intelligence explicitly separate from model training and betting logic until labels and walk-forward backtests exist.
