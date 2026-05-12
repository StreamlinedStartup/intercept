---
# intercept-dkj4
title: 'D2-HOC-C: Import target FightOdds event batch'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:37Z
updated_at: 2026-05-12T03:00:22Z
parent: intercept-vgy0
blocked_by:
    - intercept-lum1
---

Acceptance criteria:
- [x] Expand historical FightOdds imports toward 30+ UFC events.
- [x] Populate historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [x] Keep import/report tooling from writing active model_versions.



## Import Path Note
- `pnpm --filter @interceptor/db import:fightodds:range -- --from 2023-01-01 --to 2024-03-10 --limit 30` failed with `FightOdds EventsRecentQuery failed with HTTP 429`.
- A single delayed retry after 75 seconds returned the same HTTP 429.
- No partial import occurred from the blocked range command.
- Task C proceeded through the explicit `--event-pks` import path, using FightOdds sitemap/discovered event ids plus `eventByPk` metadata.

## Attempted Verification
- `psql postgres://interceptor:interceptor@localhost:5434/interceptor -c "select count(*) as events from historical_odds_events where source='fightodds';" -c "select min(event_date), max(event_date) from historical_odds_events where source='fightodds';" -c "select count(*) as fights from historical_odds_fights;" -c "select count(*) as moneylines from historical_moneyline_odds;"` => 3 events, 2024-02-24 through 2024-03-09, 46 fights, 2,173 moneylines.



## Summary of Changes
- Added explicit `--event-pks` FightOdds import mode using sitemap/discovered event ids plus `eventByPk`, avoiding the rate-limited `allEvents` pagination endpoint.
- Added `--continue-on-error` and per-event failure reporting so one source event cannot abort the whole batch.
- Imported the 30-event D2-HOC UFC target cohort into `historical_odds_events`, `historical_odds_fights`, `historical_moneyline_odds`, and `unmatched_historical_odds`.
- Matched the expanded corpus and regenerated historical odds coverage artifacts.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 5356,5318,5362,5355,5358,5347,5306,5293,4779,5281,5251,4778,5098,4777,4655,5107,4776,4775,4774,4749,4802,4755,4727,4738,4751,4744,4671,4702,4634,4696 --delay-ms 1500 --continue-on-error` => 30/30 events imported, 464 fights, 23,598 moneyline rows, 0 failed events.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all` => 26/30 events matched, 244/464 fights matched, 0 ambiguous, 13,759 linked moneyline rows.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event` => target events 30/30 imported, writes_model_versions false.
- `psql postgres://interceptor:interceptor@localhost:5434/interceptor -c "select count(*) as model_versions from model_versions;" -c "select count(*) as historical_events from historical_odds_events where source='fightodds';" -c "select count(*) as historical_fights from historical_odds_fights;" -c "select count(*) as historical_moneylines from historical_moneyline_odds;" -c "select count(*) as unmatched_historical_rows from unmatched_historical_odds where source='fightodds';"` => 14 model_versions unchanged; 30 historical events; 464 fights; 23,598 moneylines; 622 unmatched rows.
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
