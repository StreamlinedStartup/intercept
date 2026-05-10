---
# intercept-tmtz
title: '0-A: docker-compose up Postgres+Timescale, smoke connect'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:27:43Z
parent: intercept-3fqo
---

Add docker-compose.yml at repo root using timescale/timescaledb:latest-pg16, port 5432, named volume data/postgres, default db 'interceptor'. Bring up, psql in, run `SELECT extversion FROM pg_extension WHERE extname='timescaledb'`, get back a version string. KISS: just one service.

- [x] docker-compose.yml committed
- [x] `docker compose up -d` brings up healthy
- [x] psql round-trip confirms timescaledb extension loaded
- [x] Add data/postgres to .gitignore

Notes: pg port 5432 is currently in-use on this machine — either map host port 5433 or stop the existing pg first. Decide at implementation time.

## Summary of Changes

- Added a `postgres` service to `docker-compose.yml` using `timescale/timescaledb:latest-pg16`, named container `interceptor-postgres`, bind-mounted volume `./data/postgres`, default DB/user/password all `interceptor`, healthcheck via `pg_isready`.
- **Host port mapping: `5434:5432`** (NOT 5432 or 5433). Both were already bound on this machine: 5432 by a local Postgres + OrbStack, 5433 also by OrbStack. The `DATABASE_URL` for downstream phases must therefore be `postgres://interceptor:interceptor@localhost:5434/interceptor`.
- `.gitignore` already has `/data/` which covers `data/postgres` — no change needed (and adding a redundant entry would be cruft per KISS).
- Smoke verified: container reports `Up (healthy)`; `psql -c "SELECT extversion FROM pg_extension WHERE extname='timescaledb'"` returns `2.26.4`.
- The pre-existing `api` service block was left untouched (unrelated to Phase 0).
