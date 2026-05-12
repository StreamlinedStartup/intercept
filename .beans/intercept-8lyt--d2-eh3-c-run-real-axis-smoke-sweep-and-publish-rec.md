---
# intercept-8lyt
title: 'D2-EH3-C: Run real-axis smoke sweep and publish recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:20:37Z
updated_at: 2026-05-12T22:50:00Z
parent: intercept-8423
blocked_by:
    - intercept-dr0p
---

Acceptance criteria:
- [x] Run a compact real-axis smoke sweep through the extended harness.
- [x] Publish JSON/Markdown output and recommendation artifacts.
- [x] Record whether any candidate clears the market gate and whether the new axes should be expanded.
- [x] Verify model_versions count remains unchanged and close the epic without HTTP/UI smoke unless a surface was added.

## Summary of Changes

- Ran `configs/experiments/market-grid-real-axes-smoke.json` through the extended harness.
- Published `data/experiments/harness/market-grid-real-axes-smoke.json`, `.md`, and recommendation artifacts.
- Recorded that no candidate cleared the market gate; the new real axes are working and should be expanded in follow-up sweeps.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-real-axes-smoke.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-real-axes-smoke.json data/experiments/harness/market-grid-real-axes-smoke-recommendation.json`
- `jq '{variant_count: (.variants | length), coverage, recommendation, top_ranked: .ranking[0:10], market_baseline}' data/experiments/harness/market-grid-real-axes-smoke.json`
- `rg -n "logistic_c_025_temperature_150_blend_10|research_only|model_params|calibration|feature_names|market gate|model_versions" data/experiments/harness/market-grid-real-axes-smoke.*`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
