---
# intercept-xbke
title: 'D2-HO-F: Expand historical odds backfill to many events'
status: completed
type: task
created_at: 2026-05-11T17:12:07Z
updated_at: 2026-05-11T18:44:00Z
parent: intercept-5rw9
blocked_by:
    - intercept-qo0o
---

Acceptance criteria:
- [x] Expand from the proven one-event path to multiple historical UFC events using the discovered source index or event-list route.
- [x] Use polite throttling, cache-aware fetches, and source-specific rate limits.
- [x] Support resumable/idempotent backfill over a bounded date range before full history.
- [x] Avoid The Odds API historical usage unless the discovery task explicitly justifies cost and rate impact.
- [x] Preserve raw source metadata and unmatched rows for every imported event.
- [x] Produce aggregate import metrics: events scanned, fights scanned, odds rows imported, matched rows, unmatched rows, and skipped rows.
- [x] Do not alter production prediction serving.

Verification:
- Run a bounded multi-event backfill and capture counts in the bean summary.
- Confirm no duplicate rows after a repeat run.
- Confirm scraper/import code does not include copied GPL or third-party scraper code.

## Summary of Changes

- Refactored `packages/db/src/import-fightodds-event.ts` so the original single-event import still works, while `pnpm --filter @interceptor/db import:fightodds:range` uses the discovered FightOdds `allEvents` GraphQL index to import multiple UFC events from a bounded date range.
- Added deterministic per-source-event import run IDs and source/fight/moneyline IDs so repeat imports update existing rows. The range command treats `--limit` as max UFC events imported, skips non-UFC FightOdds index rows, and supports `--delay-ms` throttling between event-detail imports.
- Preserved raw event/fight/offer metadata and unmatched review rows for each imported event. Null outcome objects from FightOdds are counted as skipped rows instead of failing the run.
- Left production prediction serving untouched and did not use The Odds API historical data.

Verification:
- `pnpm --filter @interceptor/db typecheck`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:range -- --from 2024-02-01 --to 2024-03-10 --limit 3 --delay-ms 100`
  - `eventsScanned: 30`
  - `eventsImported: 3`
  - `eventsSkipped: 27`
  - `fightsRead: 46`
  - `moneylinesRead: 2173`
  - `matchedRows: 0`
  - `unmatchedRows: 46`
  - `skippedRows: 131`
  - `cancelledFights: 9`
  - `sourceEventIds: ["5356", "5318", "5362"]`
- Re-ran the same bounded import; counts remained stable at 3 historical events, 46 historical fights, 2173 moneyline rows, and 0 duplicate moneyline keys.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event` still imports event `5362`; event `5362` remained matched to canonical event `902ab9197b83d0db` with 12 of 14 source fights matched afterward.
- `pnpm --filter @interceptor/db test`
- `rg -n "GPL|github|scraper|fightodds" packages/db/src/import-fightodds-event.ts packages/db/package.json` showed only local FightOdds command/API references and no copied GPL or third-party scraper code.
