---
# intercept-41ei
title: 'D2-HO-G: Final odds-aware verification and report'
status: completed
type: task
created_at: 2026-05-11T17:12:14Z
updated_at: 2026-05-11T19:01:00Z
parent: intercept-5rw9
blocked_by:
    - intercept-xbke
---

Acceptance criteria:
- [x] Produce final odds-aware evaluation artifacts, preferably data/experiments/odds-aware-evaluation.json and data/experiments/odds-aware-evaluation.md.
- [x] Report ROI by flat stake, edge bucket, confidence bucket, and market-favorite baseline.
- [x] Report no-vig edge, calibration versus market, and closing-line value if the source provides open/close or timestamped lines.
- [x] Include secondary model-quality context: accuracy, log loss, Brier score, and ROC AUC.
- [x] Document source coverage, unmatched rate, timestamp limitations, and whether FightOdds.io remains the recommended historical source.
- [x] Verify production predictions were not changed by this research epic.
- [x] Decide whether an agent-browser smoke bean is required based on whether any HTTP or UI surface was added.

Verification:
- Run focused unit/integration tests for importer, matcher, odds math, and report generation.
- Run the final report command and commit generated evidence.
- If HTTP/UI was added, create and complete a final D2-HO-Sm agent-browser smoke gate with screenshot evidence under data/smoke/ before closing the epic.

## Summary of Changes

- Added final odds-aware evaluation mode to `services/python/ml/odds_aware_report.py` and wired `pnpm --filter @interceptor/db report:odds-aware:evaluation`.
- Generated and committed `data/experiments/odds-aware-evaluation.json` plus `data/experiments/odds-aware-evaluation.md`.
- Final coverage: 3 FightOdds events imported, 1 canonical event matched, 2 source events unmatched, 46 source fights imported, 12 source fights matched, 2173 moneyline rows imported, 600 moneyline rows linked to canonical fighters, 1 event and 12 fights scored.
- Final model-edge selections were 0-6 for -100.0% ROI; market-favorite baseline was 10-12 for +31.4% ROI. Secondary model metrics were 41.7% accuracy, 0.7087 log loss, 0.2576 Brier score, and 0.4571 ROC AUC.
- Closing-line value is reported unavailable because FightOdds `source_current` is scrape-time current/close-like consensus and `source_previous` has no timestamp. FightOdds remains the recommended source; canonical matching coverage is the current blocker.
- No smoke Bean is required because this epic added DB/Python research commands and generated artifacts only; no HTTP route or UI surface was added.

Verification:
- `services/python/.venv/bin/python -m pytest services/python/test_odds_aware_report.py -q`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:odds-aware:evaluation`
- `git diff --name-only` showed only `AGENTS.md`, `packages/db/package.json`, and `services/python/ml/odds_aware_report.py` before staging; production prediction-serving files were not touched.
