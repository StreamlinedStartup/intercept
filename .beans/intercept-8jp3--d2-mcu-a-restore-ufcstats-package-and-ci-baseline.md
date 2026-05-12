---
# intercept-8jp3
title: 'D2-MCU-A: Restore UFCStats package and CI baseline'
status: todo
type: task
priority: high
created_at: 2026-05-12T03:33:18Z
updated_at: 2026-05-12T03:33:18Z
parent: intercept-p6uo
---

Acceptance criteria:
- [ ] Resolve the fork/main build failure around @interceptor/domain-ufcstats by restoring the missing workspace package or removing the stale registration through an explicit product decision.
- [ ] Verify pnpm workspace resolution includes every registered domain package.
- [ ] Run the focused API/db build or full CI gate far enough to prove the ufcstats package issue is gone.
- [ ] Preserve the original checkout dirty AGENTS.md and stashes.

Notes:
- This is required before more model work because broken CI makes model evidence hard to trust.
