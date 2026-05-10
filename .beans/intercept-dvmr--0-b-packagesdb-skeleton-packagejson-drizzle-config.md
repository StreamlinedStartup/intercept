---
# intercept-dvmr
title: '0-B: packages/db skeleton (package.json + drizzle config)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:31:16Z
parent: intercept-3fqo
blocked_by:
    - intercept-tmtz
---

Create the workspace package only — no schema yet. Just enough to run `pnpm install` and have the package resolvable.

- [x] packages/db/package.json (name @interceptor/db, deps drizzle-orm + postgres + drizzle-kit dev)
- [x] packages/db/drizzle.config.ts
- [x] packages/db/tsconfig.json
- [x] pnpm install passes; pnpm --filter @interceptor/db typecheck (empty package) passes

## Summary of Changes

- `packages/db/package.json` — `@interceptor/db`, deps `drizzle-orm@0.36.4` + `postgres@3.4.5`, devDeps `drizzle-kit@0.28.1` + `tsx` + `typescript`. Scripts: `build`, `typecheck`, `generate`, `migrate`.
- `packages/db/drizzle.config.ts` — points at `./src/schema.ts`, output `./migrations`, dialect `postgresql`, default `DATABASE_URL` `postgres://interceptor:interceptor@localhost:5434/interceptor` (matches the host port 5434 the Phase 0-A container is mapped to).
- `packages/db/tsconfig.json` — extends `tsconfig.base.json`, `rootDir` `./src`. NOT including `drizzle.config.ts` because tsc enforces `rootDir` and the config sits at the package root; drizzle-kit reads it directly via tsx so it doesn't need to be in the typecheck program.
- `packages/db/src/index.ts` — empty placeholder (`export {}`) so the package is importable without errors before schema lands in 0-C.
- `pnpm install` — clean, no errors. `pnpm --filter @interceptor/db typecheck` — clean.
