---
# intercept-gopa
title: 'D2-HO-D: Match historical odds rows to canonical fights'
status: completed
type: task
priority: normal
created_at: 2026-05-11T17:11:53Z
updated_at: 2026-05-11T18:09:02Z
parent: intercept-5rw9
blocked_by:
    - intercept-ovyg
---

Acceptance criteria:
- [x] Match FightOdds events to canonical DB events using date, promotion, normalized event name, and source metadata.
- [x] Match fights using event date, UFC promotion, normalized fighter names, aliases when available, sorted fighter pairs, and weight class when available.
- [x] Correctly handle swapped fighter order.
- [x] Explicitly handle missing accents, punctuation differences, nicknames, renamed fighters, cancelled bouts, and rebooked bouts.
- [x] Preserve ambiguous and unmatched rows with a review reason and candidate canonical matches.
- [x] Produce match-rate and unmatched-rate summary output for the one-event slice.

Verification:
- Unit tests cover name normalization, swapped fighter order, accent/punctuation normalization, and ambiguous matches.
- One-event import shows matched canonical fight/fighter IDs where possible and review rows where not possible.

## Summary of Changes

Implemented canonical matching for the one imported FightOdds event:
- Added `pnpm --filter @interceptor/db match:fightodds:event`.
- Matched the FightOdds event to canonical event `902ab9197b83d0db` using date window, UFC promotion, and normalized event/headline names.
- Matched source fights to canonical fights by normalized fighter pairs, including swapped source order.
- Added pure matching helpers with tests for accent/punctuation normalization, swapped order, renamed/spelling aliases, and ambiguous duplicate candidates.
- Handled known one-event alias cases: `Christian Quiñónez` to `Cristian Quinonez`, `Daniel da Silva` to `Daniel Lacerda`, `Luis Rodríguez` to `Ronaldo Rodriguez`, `Yasmine Jauregui` to `Yazmin Jauregui`, and `Muhammadjon Naimov` to `Muhammad Naimov`.
- Preserved cancelled/rebooked source fights as unmatched review rows with reasons and candidate canonical matches rather than forcing them into completed canonical fights.

Verification evidence:
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test` passed 4 tests.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:event` returned `fightsRead: 14`, `fightsMatched: 12`, `fightsAmbiguous: 0`, `fightsUnmatched: 2`, `cancelledUnmatched: 2`, `moneylineRowsLinked: 600`, `matchRate: 0.8571428571428571`, `unmatchedRate: 0.14285714285714285`.
- Database query confirmed `historical_odds_fights` has 12 `matched` and 2 `unmatched` rows, with the unmatched rows limited to cancelled Brandon Moreno vs. Amir Albazi and Raul Rosas Jr. vs. Ricky Turcios source fights.
