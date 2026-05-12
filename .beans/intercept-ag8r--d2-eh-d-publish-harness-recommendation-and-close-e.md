---
# intercept-ag8r
title: 'D2-EH-D: Publish harness recommendation and close epic'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:13:36Z
updated_at: 2026-05-12T06:49:00Z
parent: intercept-ls80
blocked_by:
    - intercept-bflx
---

Acceptance criteria:
- [x] Publish final JSON/Markdown recommendation describing how to use the harness and what the first matrix found.
- [x] State whether MLflow is needed now or later.
- [x] Record verification commands and model_versions count.
- [x] Close the epic without HTTP/UI smoke gate unless a UI/API surface was added.

## Summary of Changes

- Published `data/experiments/harness/experiment-harness-recommendation.json` and `data/experiments/harness/experiment-harness-recommendation.md`.
- Recorded that MLflow is a later-layer tracking UI, not required before the config-driven harness registry.
- Documented that the epic has no HTTP/UI smoke gate because it added only a pure Python report-only CLI and committed artifacts.

## Verification

- `jq empty data/experiments/harness/market-grid-smoke.json data/experiments/harness/market-grid-summary.json data/experiments/harness/experiment-harness-recommendation.json`
- `rg -n "MLflow|research_only|model_versions|No HTTP/UI smoke gate|blend_25_availability_75_market" data/experiments/harness/experiment-harness-recommendation.* docs/experiment_harness.md`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
