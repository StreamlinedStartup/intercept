---
# intercept-nzo1
title: Sync upcoming UFC cards into DB before odds matching
status: completed
type: task
priority: normal
created_at: 2026-05-09T21:58:17Z
updated_at: 2026-05-09T23:59:06Z
parent: intercept-8gxf
blocked_by:
    - intercept-qjks
---

Seed canonical upcoming event/fight/fighter rows from ufcstats upcoming events before relying on high odds match rates.

Acceptance:
- [x] Fetch /api/ufcstats/events/upcoming and each /api/ufcstats/event/:id.
- [x] Upsert upcoming events, fights, fighters, and pending fight rows sufficient for odds matching.
- [x] Re-run /api/odds-mma/snapshot and verify match rate is meaningful against live upcoming cards.
- [x] Document any remaining unmatched odds rows with reasons.

## Summary of Changes

- Added `POST /api/predict/sync/upcoming-cards` to refresh UFCStats upcoming cards and upsert upcoming events, fighters, fights, and pending participant rows.
- Wired `/api/odds-mma/snapshot` to run the upcoming-card sync before loading the canonical fight match index.
- Verified live sync inserted 8 upcoming events, 53 fights, 106 fighters, and 106 pending participant rows with no skipped fights.
- Verified live odds snapshot matched 48 odds rows across 6 canonical `UFC Freedom 250` fights.

## Remaining Unmatched Odds Rows

- Snapshot `2026-05-09T23:58:18.454Z` logged 47 unmatched odds events.
- All 47 rows have reason `no canonical fight for date and fighter pair`.
- The unmatched rows are market-only/speculative or out-of-current-UFCStats-card pairs, including old same-day odds (`2026-05-09`/`2026-05-10`), non-canonical fantasy pairs such as `Gina Carano vs Ronda Rousey`, and future/out-of-card title speculation such as `Conor McGregor vs Michael Chandler` and `Kamaru Usman vs Islam Makhachev`.

## Verification

- `pnpm --filter @interceptor/api typecheck`
- `pnpm biome check --write apps/api/src/routes/upcoming-sync.ts apps/api/src/index.ts domains/odds-mma/src/routes.ts .beans/intercept-nzo1--sync-upcoming-ufc-cards-into-db-before-odds-matchi.md`
- `curl -sS -X POST http://127.0.0.1:3001/api/predict/sync/upcoming-cards`
- `curl -sS http://127.0.0.1:3001/api/odds-mma/snapshot`
- `docker exec -i interceptor-postgres psql -U interceptor -d interceptor -c "SELECT e.date, e.name, count(DISTINCT f.id) AS fights, count(*) AS odds_rows FROM odds_snapshots os JOIN fights f ON f.id = os.fight_id JOIN events e ON e.id = f.event_id WHERE os.snapshot_at = '2026-05-09T23:58:18.454Z' GROUP BY e.date, e.name ORDER BY e.date, e.name;"`
