---
# intercept-0asz
title: 'D2-MCU-C: Import and rematch completion event batch'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:33:31Z
updated_at: 2026-05-12T03:46:06Z
parent: intercept-p6uo
blocked_by:
    - intercept-zlwa
---

Acceptance criteria:
- [x] Import the approved completion candidate FightOdds events into historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [x] Run deterministic event/fight rematching after import.
- [x] Preserve cancelled-bout handling and unresolved reason reporting.
- [x] Report imported events, imported fights, matched fights, linked moneyline rows, and failed imports.

Constraints:
- Keep importer/report tooling report-only for model validation purposes.
- Do not write active model_versions.

## Summary of Changes

- Imported 7 supplemental FightOdds UFC events with 108 source fights and 5,458 moneyline rows.
- Ran deterministic all-event rematching; corpus now has 31 matched source events, 299 matched fights, and 16,912 linked moneyline rows.
- Published import-batch and post-import coverage JSON/Markdown reports while preserving unresolved review reasons.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 4594,4615,4627,4643,4654,4666,4668 --delay-ms 1500 --continue-on-error`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --output data/experiments/market-coverage-unlock-post-import-coverage.json --markdown data/experiments/market-coverage-unlock-post-import-coverage.md`
- `jq empty data/experiments/market-coverage-unlock-import-batch.json`
