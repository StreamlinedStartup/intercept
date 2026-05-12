---
# intercept-28c6
title: 'D2-EH-A: Define experiment config and run contract'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:13:36Z
updated_at: 2026-05-12T06:18:00Z
parent: intercept-ls80
---

Acceptance criteria:
- [x] Define a checked-in config schema and example matrix for report-only market experiments.
- [x] Capture corpus/version inputs, split policy, model variants, feature transforms, market blend options, and gate thresholds.
- [x] Document guardrails against repeated-final-holdout overfitting.
- [x] No model_versions writes.

## Summary of Changes

- Added `configs/experiments/market-experiment.schema.json`.
- Added `configs/experiments/market-grid.example.json` with a small model/feature/blend matrix.
- Documented the harness contract and overfitting guardrails in `docs/experiment_harness.md`.

## Verification

- `jq empty configs/experiments/market-experiment.schema.json configs/experiments/market-grid.example.json`
- `python - <<'PY' ... PY` checked report-only, research-only, chronological split, market baseline, and variant count fields.
- `rg -n "chronological|research_only|model_versions|MLflow|market favorite|locked|schema|market-grid" configs/experiments docs/experiment_harness.md`
