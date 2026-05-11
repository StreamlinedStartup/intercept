---
# intercept-ovyg
title: 'D2-HO-C: Import one FightOdds event moneyline slice'
status: completed
type: task
priority: normal
created_at: 2026-05-11T17:11:46Z
updated_at: 2026-05-11T17:57:06Z
parent: intercept-5rw9
blocked_by:
    - intercept-t19g
---

Acceptance criteria:
- [x] Implement only the UFC Fight Night 237 / Moreno vs Royval 2 import slice from the approved source shape.
- [x] Import moneyline odds for the candidate event without broad pagination or many-event scraping.
- [x] Persist source event/fight IDs, source URLs, raw fighter names, sportsbook when available, American odds, decimal odds, and raw metadata.
- [x] Make the import idempotent for repeat local runs.
- [x] Preserve unmatched or ambiguous rows for review rather than dropping them.
- [x] Keep production prediction serving unchanged.

Verification:
- Import command or script reports rows read, rows inserted/updated, rows matched, and rows unmatched.
- Database query confirms only the one target event was imported.
- Tests or focused command output verify American-to-decimal conversion if conversion is implemented here.

## Summary of Changes

Implemented a dedicated historical FightOdds import slice for only UFC Fight Night 237 / Moreno vs. Royval 2 (`source_event_id = 5362`):
- Added historical odds tables for import runs, source events, source fights, source moneyline rows, and unmatched historical odds review rows.
- Added `pnpm --filter @interceptor/db import:fightodds:event`, which calls the single discovered `EventOddsQuery` with `eventPk: 5362` and does not paginate event lists or scrape additional events.
- Persisted source event/fight/fighter IDs, source URLs, raw fighter names, sportsbook IDs/slugs/names, source-current and source-previous American odds, derived decimal/implied values, timestamp semantics, and raw JSON metadata.
- Made repeat imports deterministic via stable IDs and upserts.
- Preserved all fight-level canonical matching as unmatched review state for `intercept-gopa` rather than guessing matches in this task.
- Left production `odds_snapshots` and prediction-serving code untouched.

Verification evidence:
- `pnpm --filter @interceptor/db typecheck`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db migrate`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event` returned `eventsRead: 1`, `fightsRead: 14`, `moneylinesRead: 652`, `rowsUpserted: 681`, `matchedRows: 0`, `unmatchedRows: 14`, `cancelledFights: 2`.
- Re-running the same import returned the same counts, verifying local idempotency.
- Database query confirmed `historical_odds_events` has exactly one imported event for `source_event_id = '5362'`, `historical_odds_fights` has 14 fights for that event, `historical_moneyline_odds` has 338 `source_current` and 314 `source_previous` rows, and `unmatched_historical_odds` has 14 review rows.
- Focused conversion output: `+120 => decimal 2.2, implied 0.45454545454545453`; `-150 => decimal 1.6666666666666665, implied 0.6`.
