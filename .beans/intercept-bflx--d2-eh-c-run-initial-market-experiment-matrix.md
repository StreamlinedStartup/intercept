---
# intercept-bflx
title: 'D2-EH-C: Run initial market experiment matrix'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:13:36Z
updated_at: 2026-05-12T06:38:00Z
parent: intercept-ls80
blocked_by:
    - intercept-9nqj
---

Acceptance criteria:
- [x] Run a small but useful harness matrix on the current market-covered corpus.
- [x] Include current XGBoost, availability-augmented XGBoost, logistic baseline, and market blends.
- [x] Publish JSON/Markdown run outputs and ranking against market favorite.
- [x] Keep value_status research_only unless a predeclared gate passes; no model_versions writes.

## Summary of Changes

- Ran the initial market experiment grid on the current market-covered corpus.
- Published summary artifacts in `data/experiments/harness/market-grid-summary.json` and `data/experiments/harness/market-grid-summary.md`.
- Recorded that the best configured candidate remains `research_only` because it did not clear the market favorite gate.

## Verification

- `jq empty data/experiments/harness/market-grid-summary.json data/experiments/harness/market-grid-smoke.json`
- `rg -n "blend_25_availability_75_market|research_only|model_versions|market favorite|XGBoost|logistic|blends" data/experiments/harness/market-grid-summary.*`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
