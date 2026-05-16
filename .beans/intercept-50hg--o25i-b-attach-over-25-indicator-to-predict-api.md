---
# intercept-50hg
title: 'O25I-B: Attach Over 2.5 indicator to predict API'
status: todo
type: task
priority: normal
created_at: 2026-05-16T05:21:03Z
updated_at: 2026-05-16T05:21:09Z
parent: intercept-ptdd
blocked_by:
    - intercept-rb6z
---

Acceptance criteria:
- [ ] Extend prediction responses with an optional Over 2.5 report-only indicator.
- [ ] Load no-vig OVERUNDER_2.5 market probability when available.
- [ ] Preserve prediction persistence behavior for winner predictions only; do not write prop indicator rows.
