---
# intercept-4rxh
title: 'D2-EH2-A: Generate expanded sweep config'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:36:08Z
updated_at: 2026-05-12T06:44:00Z
parent: intercept-k0yc
---

Acceptance criteria:
- [x] Create a checked-in expanded harness config with dozens of curated variants.
- [x] Include market favorite, XGBoost, availability-augmented XGBoost, logistic baselines, and multiple market blend weights.
- [x] Keep config report_only, research_only, chronological, and market-gated.
- [x] Validate the config JSON and variant count before running the sweep.

## Summary of Changes

- Added `scripts/experiments/generate-expanded-market-grid.mjs` so the expanded config can be regenerated.
- Generated `configs/experiments/market-grid-expanded-100.json` with 103 variants: one market favorite baseline plus dense blend sweeps for production XGBoost, availability-augmented XGBoost, and logistic regression.
- Kept the expanded config `research_only`, report-only, chronological, and market-gated against the market favorite baseline.

## Verification

- `node scripts/experiments/generate-expanded-market-grid.mjs`
- `jq '.variants | length' configs/experiments/market-grid-expanded-100.json` => `103`
- `jq empty configs/experiments/market-grid-expanded-100.json`
- Python assertions checked uniqueness, policy fields, model families, and exactly one market favorite baseline.
