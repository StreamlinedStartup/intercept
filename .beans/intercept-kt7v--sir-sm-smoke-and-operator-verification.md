---
# intercept-kt7v
title: 'SIR-Sm: Smoke and operator verification'
status: todo
type: task
created_at: 2026-05-16T05:58:36Z
updated_at: 2026-05-16T05:58:36Z
parent: intercept-qh8w
blocked_by:
    - intercept-qhy2
    - intercept-e042
    - intercept-yenm
    - intercept-v21k
---

Close out the scheduled indicator pipeline with focused verification and browser smoke evidence.

Acceptance criteria:
- [ ] Focused DB/API/Python/UI tests pass for snapshot-backed indicators and scheduled command surfaces.
- [ ] Manual operator command path is documented with expected output and failure modes.
- [ ] agent-browser smoke verifies /upcoming renders snapshot-backed Over 2.5 states and saves a screenshot under data/smoke/.
- [ ] Verify no automatic betting activation and no unintended prop prediction writes.
- [ ] Complete epic summary, PR, merge, and branch/worktree cleanup.
