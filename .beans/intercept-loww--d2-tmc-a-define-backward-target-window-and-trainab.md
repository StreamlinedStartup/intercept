---
# intercept-loww
title: 'D2-TMC-A: Define backward target window and trainability baseline'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:23:34Z
updated_at: 2026-05-12T04:26:53Z
parent: intercept-ftbt
---

Acceptance criteria:
- [x] Identify the older UFC event window before the current 37-event corpus that should raise model-eligible events above 30.
- [x] Produce report-only baseline trainability counts from the current corpus: scored events, scored fights, model-eligible events, and model-eligible fights.
- [x] Record target import count and rationale in JSON/Markdown artifacts.
- [x] Do not write active model_versions.

## Summary of Changes

- Created the D2-TMC Beans graph under `intercept-8mw9`.
- Published `data/experiments/trainable-market-corpus-target-window.json` and `.md`.
- Baseline remains 37 scored market-covered events, 345 scored fights, 26 model-eligible events, and 241 model-eligible fights.
- Selected a 14-event older UFC FightOdds target window from 2023-01-14 through 2023-04-29.

## Verification

- `jq empty data/experiments/trainable-market-corpus-target-window.json`
- `rg -n "Model-eligible|2023-01-01|import:fightodds:event|Writes|model_versions" data/experiments/trainable-market-corpus-target-window.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python - <<'PY' ... select count(*) from model_versions ... PY` => `14`
