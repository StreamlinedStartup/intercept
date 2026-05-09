---
# intercept-mlzl
title: Document upstream submission ban
status: completed
type: task
created_at: 2026-05-09T23:26:08Z
updated_at: 2026-05-09T23:26:08Z
---

Add non-negotiable guidance forbidding PRs, pushes, or merges to upstream/original Interceptor remotes.

- [x] Update CLAUDE.md with upstream submission ban
- [x] Update AGENTS.md with the identical mirrored rule
- [x] Verify CLAUDE.md and AGENTS.md are byte-identical

## Summary of Changes

Added a hard remote-boundary rule to the Git workflow section. It forbids
opening PRs, pushing branches, creating cross-repo PRs, or merging this
project's work into upstream/original Interceptor repositories, including
`adam-s/intercept`.

Verification:

- `cmp -s CLAUDE.md AGENTS.md` returned identical.
