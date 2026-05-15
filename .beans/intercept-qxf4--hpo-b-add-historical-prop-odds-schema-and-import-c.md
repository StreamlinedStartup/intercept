---
# intercept-qxf4
title: 'HPO-B: Add historical prop odds schema and import contract'
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
- [ ] Add dedicated historical prop odds table or schema extension separate from odds_snapshots.
- [ ] Preserve source event/fight/market/outcome identity and raw metadata.
- [ ] Keep line_kind semantics source_current/source_previous only unless timestamps are proven.
- [ ] Add migration and TypeScript schema coverage.
