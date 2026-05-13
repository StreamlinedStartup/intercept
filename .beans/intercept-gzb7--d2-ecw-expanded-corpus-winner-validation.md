---
# intercept-gzb7
title: 'D2-ECW: Expanded corpus winner validation'
status: completed
type: epic
priority: high
created_at: 2026-05-13T00:21:19Z
updated_at: 2026-05-13T00:48:00Z
---

Retest the gate-clearing selected-fight candidate across broader corpus windows and search for additional report-only winners. Keep outputs research_only, do not write model_versions, and compare selected candidates against same-subset market baselines.

## Summary of Changes

- Retested the original gate-clearing winner across five broader corpus windows.
- Confirmed it clears every window from `min_train_samples=20` to 100.
- Added a 7,777-variant selected-fight search at the broader `min_train_samples=20` corpus.
- Found 150 additional market-gate-clearing variants.
- Published compact JSON/Markdown summaries and a recommendation doc.

## Verification

- `winner-expanded-corpus-mintrain-{20,40,60,80,100}.json` -> all `candidate_for_locked_evaluation`.
- Original winner at `min_train_samples=20`: 49 events, 268 selected fights, +2.74% ROI delta, -0.0126 log-loss delta, -0.0062 Brier delta.
- Additional winner search: 7,777 variants, 150 clearing variants.
- Top additional winner: `log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66`, 48 events, 228 selected fights, +3.67% ROI delta, -0.0231 log-loss delta, -0.0107 Brier delta.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_generate_exhaustive_market_matrix.py -q` -> 5 passed.
- HTTP/UI smoke gate not required: pure research/reporting epic with no endpoint or UI surface.
