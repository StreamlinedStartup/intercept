---
# intercept-on0t
title: 'D2-TMC-B: Import older FightOdds target batch'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:23:40Z
updated_at: 2026-05-12T04:29:45Z
parent: intercept-ftbt
blocked_by:
    - intercept-loww
---

Acceptance criteria:
- [x] Import the selected older UFC FightOdds event batch using historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [x] Preserve deterministic import behavior and report import counts.
- [x] Do not modify UI/API behavior or write active model_versions.

## Summary of Changes

- Imported the 14-event older UFC FightOdds target batch from 2023-01-14 through 2023-04-29.
- Added 209 historical odds fights and 10,966 historical moneyline rows for the target batch.
- Published `data/experiments/trainable-market-corpus-import-summary.json` and `.md`.
- Confirmed `model_versions` remained unchanged at 14 rows.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 4592,4579,4580,4556,4501,4483,4486,4450,4469,4460,4438,4441,4382,4426 --delay-ms 1500 --continue-on-error`
- `jq empty data/experiments/trainable-market-corpus-import-summary.json`
- `rg -n "Events imported|Events failed|Target fights|model_versions|Matching remains" data/experiments/trainable-market-corpus-import-summary.md`
