---
# intercept-p6uo
title: 'D2-MCU: Market coverage unlock to 30 scored events'
status: completed
type: epic
priority: high
created_at: 2026-05-12T03:33:06Z
updated_at: 2026-05-12T03:56:41Z
parent: intercept-8mw9
---

Restore a green baseline, finish market-covered event coverage, and rerun the validation gate so model-improvement work has enough scored events to proceed responsibly.

Acceptance criteria:
- [x] CI/package baseline is green or the remaining blocker is isolated and documented before corpus work continues.
- [x] Coverage-completion candidates are selected from unresolved D2-HOC gaps and/or adjacent FightOdds UFC events.
- [x] Historical odds imports and rematching reach at least 30 scored market-covered UFC events or publish a reportable blocker.
- [x] Leakage audit, baselines, coverage, and market gate are rerun after the coverage-completion work.
- [x] Final unlock report states whether model-improvement experiments are unblocked.

Constraints:
- Keep all reports research-only unless the market gate truly passes.
- Do not tune XGBoost in this epic.
- Do not activate validated status unless coverage and ROI thresholds truly pass.
- Do not write active model_versions.
- Preserve unrelated dirty files and stashes.

## Summary of Changes

- Restored the tracked UFCStats domain package and fixed local CI environment propagation so the baseline is green.
- Selected, imported, and rematched the coverage-completion FightOdds batch, then added event-alias matching for ESPN/ABC and numbered Fight Night source names.
- Expanded historical odds coverage to 37/37 matched source events, 345 scored market-covered fights, and 37 scored market-covered events.
- Published final unlock reports showing research-only model-improvement experiments are unblocked while validated/value activation remains blocked.

## Outcome

- Coverage gate passed: 345 scored fights >= 200 and 37 scored events >= 30.
- Leakage audit passed: 15/15 checks.
- Activation gate did not pass: model pick ROI was -10.4%, market favorite ROI was +16.2%, and the best blend ROI was +15.9%, below market favorite by 0.3pp rather than above it by +2pp.
- No active `model_versions` writes were performed.

## Verification

- `./scripts/ci-local.sh`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --include-db --output data/experiments/market-coverage-unlock-leakage-audit.json --markdown data/experiments/market-coverage-unlock-leakage-audit.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.market_gate_report --output data/experiments/market-coverage-unlock-market-gate-report.json --markdown data/experiments/market-coverage-unlock-market-gate-report.md`
- `jq empty data/experiments/market-coverage-unlock-final-report.json`
