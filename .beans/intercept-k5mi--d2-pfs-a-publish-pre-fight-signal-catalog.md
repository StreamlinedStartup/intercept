---
# intercept-k5mi
title: 'D2-PFS-A: Publish pre-fight signal catalog'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:39:50Z
updated_at: 2026-05-12T22:47:00Z
parent: intercept-8o0d
---

Acceptance criteria:
- [x] Publish JSON/Markdown catalog of pre-fight-only signal candidates.
- [x] For each signal, define source data, leakage posture, feature semantics, implementation readiness, and validation gate.
- [x] Separate existing-data candidates from new-data candidates.
- [x] Recommend the next smallest justified experiment and keep all candidates research_only.

## Summary of Changes

- Published `data/experiments/pre-fight-signal-candidates.json` and `.md`.
- Added `docs/pre_fight_signal_catalog.md` as the operator-facing pointer.
- Recommended `opponent_adjusted_recent_performance_v1` as the next smallest justified report-only experiment.

## Verification

- `jq empty data/experiments/pre-fight-signal-candidates.json`
- `rg -n "opponent_adjusted_recent_performance_v1|line_movement_microstructure_v1|feature_availability_flags_v1|research_only|model_versions" data/experiments/pre-fight-signal-candidates.* docs/pre_fight_signal_catalog.md`
