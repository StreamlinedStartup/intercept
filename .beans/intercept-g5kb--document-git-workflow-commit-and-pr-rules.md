---
# intercept-g5kb
title: Document git workflow commit and PR rules
status: completed
type: task
priority: normal
created_at: 2026-05-09T20:38:38Z
updated_at: 2026-05-09T20:39:13Z
---

Add non-negotiable commit-per-task and PR-per-epic rules plus concise commit/PR templates to CLAUDE.md and AGENTS.md.

- [x] CLAUDE.md documents the workflow rules
- [x] AGENTS.md mirrors CLAUDE.md
- [x] Commit template is concise and verification-first
- [x] PR template is scoped to one epic and token-aware

## Summary of Changes

Added non-negotiable Git workflow rules and compact commit/PR templates to both mirrored agent instruction files.

Verification:
- cmp -s CLAUDE.md AGENTS.md returned 0
- rg confirmed Git workflow, Commit template, and PR template sections in both files
