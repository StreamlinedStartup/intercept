---
# intercept-xsmv
title: 'D2-TMC-D: Rerun expanded coverage and market gate'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:23:55Z
updated_at: 2026-05-12T04:38:41Z
parent: intercept-ftbt
blocked_by:
    - intercept-lgvs
---

Acceptance criteria:
- [x] Rerun historical odds coverage, leakage audit, simple baselines, and market gate reports.
- [x] Report scored events, scored fights, moneyline linkage, market favorite ROI, model/blend ROI, and value_status.
- [x] Keep status research_only unless activation truly passes; no active model_versions writes.

## Summary of Changes

- Published expanded coverage, leakage audit, simple baseline, and market gate reports under `data/experiments/trainable-market-corpus-*`.
- Expanded market-covered evaluation to 51 scored events and 486 scored fights.
- Leakage audit passed 15/15 checks.
- Market favorite ROI is +20.0%; model pick ROI is -11.2%; best simple blend ROI is +18.5%, still -1.5pp versus market favorite.
- Value status remains `research_only`; no active `model_versions` writes occurred.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --output data/experiments/trainable-market-corpus-coverage.json --markdown data/experiments/trainable-market-corpus-coverage.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.leakage_audit --include-db --output data/experiments/trainable-market-corpus-leakage-audit.json --markdown data/experiments/trainable-market-corpus-leakage-audit.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.baselines --output data/experiments/trainable-market-corpus-simple-baselines.json --markdown data/experiments/trainable-market-corpus-simple-baselines.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_gate_report --output data/experiments/trainable-market-corpus-market-gate-report.json --markdown data/experiments/trainable-market-corpus-market-gate-report.md`
- `jq empty data/experiments/trainable-market-corpus-coverage.json data/experiments/trainable-market-corpus-leakage-audit.json data/experiments/trainable-market-corpus-simple-baselines.json data/experiments/trainable-market-corpus-market-gate-report.json`
