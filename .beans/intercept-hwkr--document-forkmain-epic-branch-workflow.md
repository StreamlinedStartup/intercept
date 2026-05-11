---
# intercept-hwkr
title: Document fork/main epic branch workflow
status: completed
type: task
priority: normal
created_at: 2026-05-10T23:31:48Z
updated_at: 2026-05-10T23:31:59Z
---

Document the project fork/main base branch, one-epic-one-branch cadence, PR merge requirement, and branch cleanup rules in CLAUDE.md and AGENTS.md.



## Summary of Changes

- Documented that local main tracks fork/main and epic branches start from updated local main.
- Documented that epic PRs target StreamlinedStartup/intercept:main and must merge before the next epic starts.
- Documented post-merge cleanup: switch to main, update from fork/main, delete merged epic branches, prune fork/epic refs, and remove temp worktrees.

## Verification

- Compared the Git workflow sections in CLAUDE.md and AGENTS.md.
- git status --short --branch
