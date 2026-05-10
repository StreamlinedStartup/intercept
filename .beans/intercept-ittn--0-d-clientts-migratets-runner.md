---
# intercept-ittn
title: '0-D: client.ts + migrate.ts runner'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:33:11Z
parent: intercept-3fqo
blocked_by:
    - intercept-dwtm
---

Make the package usable from elsewhere.

- [x] packages/db/src/client.ts exporting db singleton from DATABASE_URL via postgres-js
- [x] packages/db/src/migrate.ts that applies pending migrations (drizzle-kit migrate equivalent)
- [x] packages/db/src/index.ts re-exports
- [x] Add 'migrate' script to packages/db/package.json

## Summary of Changes

- `packages/db/src/client.ts` — fails loud at module-load if `DATABASE_URL` is unset (per "fail loud, never silent" in CLAUDE.md). Exports `db` (drizzle instance bound to the schema) and raw `sql` (postgres-js client) plus a `Database` type alias.
- `packages/db/src/migrate.ts` — standalone migration runner using `drizzle-orm/postgres-js/migrator`, masks password in the log line, exits 1 if `DATABASE_URL` missing.
- `packages/db/src/index.ts` — re-exports schema + `db`/`sql`/`Database`.
- `packages/db/package.json` — `migrate` script was added in 0-B (`tsx src/migrate.ts`); confirmed wired.
- Smoke: `DATABASE_URL=… pnpm --filter @interceptor/db migrate` printed `[migrate] done`. `\dt` in psql shows `events` + `fighters` tables in the live container — migration is real, not just a typecheck.
