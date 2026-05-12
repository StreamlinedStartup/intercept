---
# intercept-vgy0
title: 'D2-HOC: Historical odds corpus expansion and entity-resolution gate'
status: completed
type: epic
priority: high
created_at: 2026-05-12T02:27:20Z
updated_at: 2026-05-12T03:17:55Z
parent: intercept-8mw9
---

Expand the historical FightOdds corpus to the validation target and harden deterministic event/fight entity resolution before any model-improvement work.

Acceptance criteria:
- [x] 30-event UFC target cohort is defined and documented.
- [x] Baseline coverage is report-only and writes no active model_versions.
- [x] Event and fight entity-resolution heuristics are improved and regression-checked on the current 3-event corpus.
- [x] Target FightOdds event batch is imported into historical odds tables.
- [x] Unmatched historical odds rows are reviewed/rematched with unresolved reasons reportable.
- [x] Scaled coverage and market-gate reports state whether the >=200 fight / >=30 event gate passes.
- [x] Final JSON and Markdown corpus expansion report are published.

Constraints:
- Keep UI/API/docs research-only unless validation truly passes.
- Do not tune XGBoost on the current 30-fight sample.
- Do not activate validated status.
- Do not write active model_versions.
- Do not build UI unless CLI review becomes a blocker.

## Summary of Changes

- Defined the D2-HOC 30-event UFC FightOdds target cohort and report-only baseline coverage artifact.
- Improved deterministic event/fight matching, imported the target event batch, and reduced the active unresolved review queue to reportable reasons.
- Ran leakage, baseline, coverage, and market-gate reports at the expanded scale, then published final JSON/Markdown corpus expansion reports.

## Outcome

- Imported 30/30 target FightOdds events with 464 source fights and 23,598 moneyline rows.
- Matched 26/30 source events, 244/464 source fights, and 13,759/23,598 moneyline rows.
- Market gate status remains `insufficient_coverage`: 235 scored fights clears the 200-fight threshold, but 26 scored market-covered events remains below the 30-event threshold.
- Model-improvement/value claims remain blocked; no active `model_versions` writes were performed.

## Verification

- `pnpm --filter @interceptor/db test -- match-historical-odds`
- `pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --include-db`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.baselines`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.market_gate_report`
- `pnpm --filter @interceptor/db report:fightodds:final`
