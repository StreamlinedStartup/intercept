---
# intercept-nwg3
title: 'D2-MRA-A: Freeze residual-analysis inputs and baseline report'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:34:32Z
updated_at: 2026-05-12T05:41:13Z
parent: intercept-b6yf
---

Acceptance criteria:
- [x] Freeze D2-TMC artifacts as residual-analysis inputs.
- [x] Report current market/model/blend baselines from the expanded corpus.
- [x] Record input artifact paths, corpus counts, and gate thresholds in JSON/Markdown artifacts.
- [x] Do not write active model_versions.

## Summary of Changes

- Added `data/experiments/market-residual-analysis-baseline.json` and `.md`.
- Froze D2-TMC input artifact paths with SHA-256 hashes, source epic, and source commit.
- Recorded expanded-corpus counts, gate thresholds, current market/model/blend baselines, and the research-only/no-`model_versions` analysis contract.

## Verification

- `jq empty data/experiments/market-residual-analysis-baseline.json`
- `rg -n "blend_25_xgboost|Market-covered events|Minimum ROI|model_versions|research_only|writes_model_versions" data/experiments/market-residual-analysis-baseline.md data/experiments/market-residual-analysis-baseline.json`
- `shasum -a 256 data/experiments/trainable-market-corpus-*.json` confirmed frozen input hashes.
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
