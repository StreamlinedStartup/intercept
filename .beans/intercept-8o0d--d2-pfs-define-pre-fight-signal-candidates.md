---
# intercept-8o0d
title: 'D2-PFS: Define pre-fight signal candidates'
status: completed
type: epic
priority: high
created_at: 2026-05-12T22:39:42Z
updated_at: 2026-05-12T22:52:00Z
parent: intercept-8mw9
---

Define a concrete pre-fight signal catalog for the next experiments after mass search found no edge. Candidates must be pre-fight-only, grounded in existing residual failures, and separated by implementation readiness and data dependencies.

## Summary of Changes

- Published a pre-fight signal catalog in JSON and Markdown.
- Separated existing-data candidates from new-data candidates and rejected already-tested/diagnostic-only ideas.
- Recommended `opponent_adjusted_recent_performance_v1` as the next smallest justified report-only experiment.

## Verification

- `jq empty data/experiments/pre-fight-signal-candidates.json`
- `rg -n "opponent_adjusted_recent_performance_v1|line_movement_microstructure_v1|feature_availability_flags_v1|research_only|model_versions" data/experiments/pre-fight-signal-candidates.* docs/pre_fight_signal_catalog.md`

No HTTP/UI smoke gate was required because this epic added research artifacts only, not an HTTP endpoint or UI surface.
