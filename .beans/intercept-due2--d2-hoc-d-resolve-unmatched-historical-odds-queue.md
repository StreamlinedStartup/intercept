---
# intercept-due2
title: 'D2-HOC-D: Resolve unmatched historical odds queue'
status: completed
type: task
priority: high
created_at: 2026-05-12T02:27:41Z
updated_at: 2026-05-12T03:04:24Z
parent: intercept-vgy0
blocked_by:
    - intercept-dkj4
---

Acceptance criteria:
- [x] Add or use deterministic review/rematch tooling to reduce unresolved unmatched rows.
- [x] Preserve unresolved rows with explicit reason codes.
- [x] Report before/after unmatched counts and match-rate impact.



## Summary of Changes
- Made unmatched review rows idempotent per source fight during matching instead of keeping import-time placeholders.
- Deleted review rows when a source fight becomes canonically matched.
- Rewrote unmatched events' fight rows with the explicit event-level reason `no canonical event matched date/name/promotion`.
- Added review reason counts to historical odds coverage JSON and Markdown reports.

## Verification
- Before cleanup: `unmatched_historical_odds` reason counts were 450 `canonical matching pending`, 86 cancelled, 72 no canonical fight, and 14 deferred rows.
- After cleanup: review rows reduced from 622 to 220; reasons are 86 cancelled, 72 no canonical fight, and 62 no canonical event; no placeholder or deferred reasons remain.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all` => 26/30 events matched, 244/464 fights matched, 0 ambiguous, 13,759 linked moneyline rows.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
