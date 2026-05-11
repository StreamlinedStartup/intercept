---
# intercept-ebnb
title: Feature-variant experiment harness
status: completed
type: epic
priority: high
created_at: 2026-05-11T16:08:29Z
updated_at: 2026-05-11T16:50:24Z
---

Build a report-only offline experiment harness for UFC predictor feature variants. The harness compares curated feature sets through walk-forward backtests, writes compact JSON/Markdown evidence, and leaves production predictions/model_versions unchanged.

## Summary of Changes
- Completed task intercept-af5s and merged PR #10 into fork/main.
- Full experiment report found baseline remains the best probability-quality variant among finalists.
- Evidence artifacts are committed at data/experiments/feature-variants.json and data/experiments/feature-variants.md.
