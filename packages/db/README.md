# @interceptor/db

Drizzle ORM + Postgres/TimescaleDB schema and client for the UFC Fight Predictor.

## Quick start

The Postgres container is defined in the repo-root `docker-compose.yml` and
binds to host port **5434** (5432 and 5433 were both occupied on the dev
machine).

```bash
docker compose up -d postgres
export DATABASE_URL='postgres://interceptor:interceptor@localhost:5434/interceptor'

pnpm --filter @interceptor/db migrate    # apply migrations
pnpm --filter @interceptor/db smoke      # round-trip insert + select
```

## Scripts

| Script | What it does |
|---|---|
| `generate` | `drizzle-kit generate` — diffs `src/schema.ts` against `migrations/` and emits a new SQL migration |
| `migrate` | Applies all pending migrations against `DATABASE_URL` |
| `smoke` | Inserts one event + one fighter and reads them back. Verifies the package end-to-end |
| `typecheck` | `tsc --noEmit` |

## Layout

```
src/
├── schema.ts     drizzle table definitions (source of truth for the DB shape)
├── client.ts     postgres-js connection + drizzle instance (fails loud if DATABASE_URL unset)
├── migrate.ts    one-shot migration runner
├── smoke.ts      end-to-end smoke test
└── index.ts      re-exports schema + client
migrations/       drizzle-generated SQL (committed)
```

## Notes

- Hypertables (`fighter_stat_snapshots`, `odds_snapshots`, `predictions`) are
  *not* created by drizzle migrations — drizzle-kit doesn't model
  `create_hypertable()`. They will be created in a post-migration hook in
  `migrate.ts` once those tables land in Phase 0-F / 0-G.
- `DATABASE_URL` is required. The client throws at import if it's missing.
