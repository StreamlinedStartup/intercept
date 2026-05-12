---
# intercept-vmow
title: 'D2-MCU-E: Rerun validation gate at completion scale'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:33:43Z
updated_at: 2026-05-12T03:54:08Z
parent: intercept-p6uo
blocked_by:
    - intercept-p6v3
---

Acceptance criteria:
- [x] Rerun leakage audit with DB checks.
- [x] Rerun simple baselines and historical odds coverage.
- [x] Rerun market gate and record scored fights, scored events, model ROI, market-favorite ROI, and blend ROI.
- [x] Keep value_status insufficient_coverage unless both coverage thresholds pass; keep validated inactive unless all activation requirements truly pass.
- [x] Confirm report tooling does not write active model_versions.

## Summary of Changes

- Reran leakage audit, simple baselines, historical odds coverage, and market-gate reports at the completed coverage scale.
- Coverage now passes the size gate with 345 scored fights across 37 market-covered events.
- Market gate remains research-only: model pick ROI was -10.4%, market favorite ROI was +16.2%, and the best 25/75 model/market blend ROI was +15.9%, which does not beat market favorite by +2pp.
- Confirmed generated reports set `writes_model_versions: false`; `model_versions` row count remained report-only evidence at 14.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --include-db --output data/experiments/market-coverage-unlock-leakage-audit.json --markdown data/experiments/market-coverage-unlock-leakage-audit.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.baselines --output data/experiments/market-coverage-unlock-simple-baselines.json --markdown data/experiments/market-coverage-unlock-simple-baselines.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.market_gate_report --output data/experiments/market-coverage-unlock-market-gate-report.json --markdown data/experiments/market-coverage-unlock-market-gate-report.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --output data/experiments/market-coverage-unlock-validation-coverage.json --markdown data/experiments/market-coverage-unlock-validation-coverage.md`
- `jq empty data/experiments/market-coverage-unlock-leakage-audit.json data/experiments/market-coverage-unlock-simple-baselines.json data/experiments/market-coverage-unlock-market-gate-report.json data/experiments/market-coverage-unlock-validation-coverage.json`
