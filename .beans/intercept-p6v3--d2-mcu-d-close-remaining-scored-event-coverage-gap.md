---
# intercept-p6v3
title: 'D2-MCU-D: Close remaining scored-event coverage gap'
status: todo
type: task
priority: high
created_at: 2026-05-12T03:33:37Z
updated_at: 2026-05-12T03:33:37Z
parent: intercept-p6uo
blocked_by:
    - intercept-0asz
---

Acceptance criteria:
- [ ] Run coverage reporting after the completion batch.
- [ ] If scored market-covered events remain below 30, use deterministic review/rematch tooling to address event/fight misses or select a small supplemental candidate set.
- [ ] Preserve unresolved rows with explicit reasons rather than dropping them.
- [ ] End with either >=30 scored market-covered events or a reportable blocker explaining why the threshold cannot be reached from available data.

Constraints:
- No model tuning in this task.
- No active model_versions writes.
