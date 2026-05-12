---
# intercept-qkjr
title: 'D2-TMC-F: Publish expanded trainability decision report'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:24:08Z
updated_at: 2026-05-12T04:41:08Z
parent: intercept-ftbt
blocked_by:
    - intercept-687y
---

Acceptance criteria:
- [x] Publish final JSON/Markdown report with corpus expansion counts, model-eligible counts, candidate results, activation blockers, and next recommendation.
- [x] State whether model-improvement work is unblocked, still blocked, or requires a separate activation epic.
- [x] Keep UI/API/docs research-only; no active model_versions writes.

## Summary of Changes

- Published `data/experiments/trainable-market-corpus-final-report.json` and `.md`.
- Recorded that trainability is unblocked: model-eligible events increased from 26 to 40.
- Recorded that validated activation remains blocked: no candidate beats the market favorite by +2pp with non-degraded probability metrics.
- Recommended the next epic as market residual analysis and pre-fight signal discovery.

## Verification

- `jq empty data/experiments/trainable-market-corpus-final-report.json`
- `rg -n "Trainability status|research_only|Validated activation|D2-MRA|model_versions|Market gate" data/experiments/trainable-market-corpus-final-report.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python - <<'PY' ... select count(*) from model_versions ... PY` => `14`
