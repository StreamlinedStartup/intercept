---
# intercept-3eph
title: 'D2-ECW-A: Retest winner across expanded corpus windows'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:21:27Z
updated_at: 2026-05-13T00:34:00Z
parent: intercept-gzb7
---

Acceptance criteria:

- [x] Re-runs the existing gate-clearing candidate over broader eligible corpus windows.
- [x] Publishes report-only JSON/Markdown artifacts for each window.
- [x] Confirms whether the winner still clears ROI, log-loss, Brier, and coverage gates.
- [x] Keeps all outputs research_only and writes_model_versions=false.

## Summary of Changes

- Added frozen-winner config generation for `min_train_samples` windows 20, 40, 60, 80, and 100.
- Ran the original gate-clearing candidate across all five expanded corpus windows.
- Published per-window JSON/Markdown artifacts plus a compact summary.
- The winner cleared the market gate in every expanded window.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/generate_winner_expanded_corpus_configs.py`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_generate_exhaustive_market_matrix.py -q` -> 4 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.generate_winner_expanded_corpus_configs`.
- `ml.experiment_harness` for `winner-expanded-corpus-mintrain-{20,40,60,80,100}.json` -> all `candidate_for_locked_evaluation`.
