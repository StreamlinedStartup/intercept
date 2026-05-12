---
# intercept-8jp3
title: 'D2-MCU-A: Restore UFCStats package and CI baseline'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:33:18Z
updated_at: 2026-05-12T03:39:42Z
parent: intercept-p6uo
---

Acceptance criteria:
- [x] Resolve the fork/main build failure around @interceptor/domain-ufcstats by restoring the missing workspace package or removing the stale registration through an explicit product decision.
- [x] Verify pnpm workspace resolution includes every registered domain package.
- [x] Run the focused API/db build or full CI gate far enough to prove the ufcstats package issue is gone.
- [x] Preserve the original checkout dirty AGENTS.md and stashes.

Notes:
- This is required before more model work because broken CI makes model evidence hard to trust.

## Summary of Changes

- Restored the existing UFCStats domain package into tracked source and allowed `domains/ufcstats/` through `.gitignore`.
- Added `DATABASE_URL` to Turbo's allowed global environment and moved the local CI default before TypeScript tests.
- Verified the original checkout remains preserved with dirty `AGENTS.md` and untouched stashes.

## Verification

- `pnpm list --filter @interceptor/domain-ufcstats --depth 0`
- `pnpm --filter @interceptor/api build`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm turbo test --filter @interceptor/api --force`
- `./scripts/ci-local.sh`
