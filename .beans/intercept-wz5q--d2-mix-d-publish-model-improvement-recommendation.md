---
# intercept-wz5q
title: 'D2-MIX-D: Publish model-improvement recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:34:20Z
updated_at: 2026-05-12T04:16:28Z
parent: intercept-tgq5
blocked_by:
    - intercept-z2lz
---

Acceptance criteria:
- [x] Publish a final recommendation with winning candidate, market comparison, residual risks, and activation blockers.
- [x] If no candidate clears the market gate, state that model improvement remains blocked and recommend the next data/model step.
- [x] If a candidate clears the research gate, create a separate activation epic rather than writing active model_versions here.
- [x] Keep UI/API/docs research-only.

## Summary of Changes

- Published `data/experiments/market-aware-model-improvement-recommendation.json` and `.md`.
- Recorded that no blend, model-family, or feature-ablation candidate clears the no-vig market favorite +2pp ROI gate.
- Recommended the next epic as trainable market-covered corpus expansion before further activation or model promotion work.
- Verified the report remains research-only and does not write `model_versions`.

## Verification

- `jq empty data/experiments/market-aware-model-improvement-recommendation.json`
- `rg -n "research_only|Writes|Activation allowed|D2-TMC|model_versions|Gate cleared" data/experiments/market-aware-model-improvement-recommendation.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python - <<'PY' ... select count(*) from model_versions ... PY` => `14`
