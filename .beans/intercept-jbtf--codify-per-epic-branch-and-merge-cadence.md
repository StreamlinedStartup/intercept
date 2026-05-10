---
# intercept-jbtf
title: Codify per-epic branch and merge cadence
status: completed
type: bug
priority: high
created_at: 2026-05-10T17:59:30Z
updated_at: 2026-05-10T18:00:53Z
---

Add non-negotiable workflow rules requiring each completed epic to open a PR, merge before the next epic, and start each next epic from the project base branch on its own branch name.

## Summary of Changes

- Added explicit one-epic/one-branch/one-PR cadence to `CLAUDE.md` and `AGENTS.md`.
- Updated `.claude/rules/workflow.md` and `.claude/rules/base-branch.md` so Claude Code also stops on stale epic branches.
- Made epic closure require a merged project-base PR before the next epic starts.

Verified:

- `pnpm biome check CLAUDE.md AGENTS.md .claude/rules/workflow.md .claude/rules/base-branch.md .beans/intercept-jbtf--codify-per-epic-branch-and-merge-cadence.md` reported these markdown paths are ignored by Biome, so there were no formatter changes to apply.
