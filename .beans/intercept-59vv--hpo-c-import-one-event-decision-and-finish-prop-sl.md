---
# intercept-59vv
title: 'HPO-C: Import one event decision and finish prop slice'
status: todo
type: task
priority: high
created_at: 2026-05-15T23:18:56Z
updated_at: 2026-05-15T23:18:56Z
parent: intercept-1xpw
blocked_by:
    - intercept-6us4
---

Acceptance criteria:
- [ ] Extend the FightOdds importer to optionally import decision/finish prop markets for one event.
- [ ] Upsert prop rows idempotently with explicit counts and skipped-market reasons.
- [ ] Do not alter existing moneyline import semantics.
- [ ] Add focused importer tests or dry-run evidence.
