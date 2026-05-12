---
# intercept-tktt
title: 'D2-MRA-D: Define pre-fight-only signal candidates'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:35:00Z
updated_at: 2026-05-12T05:54:38Z
parent: intercept-b6yf
blocked_by:
    - intercept-ty3n
---

Acceptance criteria:
- [x] Define one or two candidate signals supported by the residual cluster evidence.
- [x] Verify each candidate uses only pre-fight information and avoids leakage/post-fight data.
- [x] Specify data source, feature semantics, expected direction, and minimum report-only validation.
- [x] If no credible candidate exists, publish a no-build recommendation instead of forcing implementation.

## Summary of Changes

- Published `data/experiments/market-residual-signal-candidates.json` and `.md`.
- Recommended one Task E build candidate: `pre_fight_feature_availability_flags`.
- Marked `market_disagreement_context` as no-build for Task E because it duplicates prior market-prior/blend experiments rather than exposing a missing internal pre-fight signal.

## Verification

- `jq empty data/experiments/market-residual-signal-candidates.json`
- `rg -n "pre_fight_feature_availability_flags|market_disagreement_context|pre_fight_only|no_build|model_versions|research_only|Task E" data/experiments/market-residual-signal-candidates.json data/experiments/market-residual-signal-candidates.md`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
