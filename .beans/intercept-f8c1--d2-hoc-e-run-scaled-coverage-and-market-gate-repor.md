---
# intercept-f8c1
title: 'D2-HOC-E: Run scaled coverage and market-gate reports'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:45Z
updated_at: 2026-05-12T03:12:10Z
parent: intercept-vgy0
blocked_by:
    - intercept-due2
---

Acceptance criteria:
- [x] Rerun leakage audit, baselines, historical odds coverage, and market gate.
- [x] Report whether coverage reaches >=200 scored fights and >=30 market-covered events.
- [x] Keep value_status insufficient_coverage unless the market gate truly passes.
- [x] Do not write active model_versions.



## Summary of Changes
- Reran leakage audit, simple baselines, historical odds coverage, and market gate against the expanded 30-event FightOdds corpus.
- Coverage crossed the fight-count threshold with 235 scored fights but did not reach the event threshold because only 26 market-covered events scored.
- Market gate remains `insufficient_coverage`; no validated status was activated.
- Report artifacts remain report-only and state `writes_model_versions: false`.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --include-db` => pass, 15/15 checks.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.baselines` => 777 events, 8,538 samples, 235 market-covered samples.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.market_gate_report` => `insufficient_coverage`, 235 scored fights across 26 events.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event` => 30/30 target events imported, 26/30 matched, 244/464 fights matched.
- JSON artifact check confirmed `writes_model_versions: false` for market gate, leakage audit, simple baselines, and historical odds target coverage.
