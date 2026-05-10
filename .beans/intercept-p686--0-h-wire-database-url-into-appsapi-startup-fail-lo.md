---
# intercept-p686
title: '0-H: Wire DATABASE_URL into apps/api startup (fail loud)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:37:48Z
parent: intercept-3fqo
blocked_by:
    - intercept-nuwf
---

Don't let the API silently boot without a DB. Crash early with a clear message.

- [x] apps/api/src/index.ts startup: import db from @interceptor/db, run `SELECT 1`, log + exit(1) on failure with a message pointing at .env.example
- [x] apps/api depends on @interceptor/db in package.json
- [x] .env.example documents DATABASE_URL (with the actual `localhost:5434` host port — see 0-A note)
- [x] README.md has a 'Database setup' section: `docker compose up -d && pnpm --filter @interceptor/db migrate`

## Summary of Changes

- `apps/api/package.json` — added `@interceptor/db: workspace:*`.
- `apps/api/src/index.ts` — `import { sql } from '@interceptor/db'` + `assertDatabaseReachable()` runs `SELECT 1` before `server.listen()`. On failure logs `[FATAL] Could not connect to the database` with the masked `DATABASE_URL` and the underlying error, then `process.exit(1)`. Note: the `@interceptor/db` client throws at module-load if `DATABASE_URL` is unset — both paths produce a clear, actionable error before the HTTP server binds.
- `.env.example` — documents `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor` (port 5434, not the plan's original 5432, because that port is already taken on the dev machine — see 0-A summary). Also placeholders for `ODDS_API_KEY` and `ADMIN_SECRET` for later phases.
- `README.md` — new "Database setup" section before "Getting Started" with the three commands (`cp .env.example .env`, `docker compose up -d postgres`, `pnpm --filter @interceptor/db migrate`) plus the smoke command. Prerequisites updated to include Docker.

## Smoke evidence

Happy path:

```
[startup] database reachable
Server listening on http://localhost:3001
```

Unset `DATABASE_URL`:

```
Error: DATABASE_URL is not set. Refusing to start without a database connection.
Set DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor (see docker-compose.yml).
Failed running 'src/index.ts'
```
