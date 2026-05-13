---
# intercept-5t8l
title: 'D2-LEV: Locked evaluation protocol'
status: completed
type: epic
priority: high
created_at: 2026-05-13T00:47:06Z
updated_at: 2026-05-13T01:16:00Z
---

Freeze the selected model candidates before evaluation, add a locked-style chronological holdout mode to the report-only market harness, run the frozen candidates without tuning, and publish the result as research_only/no model_versions.

## Summary of Changes

- Froze three candidates before evaluation.
- Added `corpus.holdout.last_n_events` support to the report-only market harness.
- Ran the frozen candidates on a last-10-event historical locked-style holdout.
- Published full and compact holdout artifacts and result docs.
- Result: no candidate cleared the locked-style holdout.

## Verification

- Candidate list froze before holdout run in `configs/experiments/locked-evaluation-candidates-v1.json`.
- Holdout config: `configs/experiments/locked-evaluation-v1.json`.
- Holdout artifact: `data/experiments/harness/locked-evaluation-v1.json`.
- Compact result: `data/experiments/harness/locked-evaluation-summary.json`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_generate_exhaustive_market_matrix.py services/python/test_experiment_harness.py -q` -> 22 passed.
- HTTP/UI smoke gate not required: pure research/reporting epic with no endpoint or UI surface.
