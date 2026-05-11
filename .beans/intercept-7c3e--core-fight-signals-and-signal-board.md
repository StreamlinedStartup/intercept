---
# intercept-7c3e
title: Core fight signals and signal board
status: completed
type: epic
priority: high
created_at: 2026-05-11T13:30:36Z
updated_at: 2026-05-11T14:13:20Z
parent: intercept-8mw9
---

Epic 1 for Decision Engine v2. Ships core decision signals through ML, API, and compare-sheet signal board. Branch: epic/<epic-id>-decision-engine-v2-core-signals.


## Summary of Changes
- Shipped Decision Engine v2 core fight signals through Python feature construction, prediction API output, and /upcoming compare-sheet UI.
- Added round-tendency and common-opponent decision signals with point-in-time leakage tests.
- Retrained local model 20260511T134646095031Z and documented observed metric deltas plus a 20-event walk-forward backtest.
- Completed agent-browser smoke evidence at data/smoke/decision-engine-v2-core-signals.png.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q
- services/python/.venv/bin/python -m pytest services/python/test_worker.py -q
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- src/routes/predict.test.ts
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- agent-browser smoke on /upcoming with compare sheet signal board screenshot
