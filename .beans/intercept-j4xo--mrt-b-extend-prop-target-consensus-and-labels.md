---
# intercept-j4xo
title: 'MRT-B: Extend prop target consensus and labels'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:46:29Z
updated_at: 2026-05-16T03:48:51Z
parent: intercept-v41p
blocked_by:
    - intercept-r3pi
---

Acceptance criteria:
- [x] Extend harness target labels for decision, finish, KO/TKO, submission, and over/under rounds where outcomes exist.
- [x] Extend prop market consensus mapping for supported method and round markets.
- [x] Keep unsupported markets explicit with coverage statuses, not silent fallbacks.
- [x] Add focused tests.

## Summary of Changes

- Extended the FightOdds prop importer to include `OVERUNDER_*` markets and classify them as `fight_round_total`.
- Added report-only harness targets for KO/TKO, submission, and over/under 0.5/1.5/2.5/3.5/4.5 rounds.
- Added target labels from fight result method/round/time and market consensus from DISTANCE, OVERUNDER, and fight-level method odds.
- Imported over/under markets for all 31 currently prop-backed FightOdds events.
