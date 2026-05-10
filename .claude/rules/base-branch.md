---
description: main is the only permanent branch — epic branches are disposable after merge
---

# Main Is the Only Branch

**`main` is the product. Epic branches are temporary delivery vehicles.**

| Lives on `main` (permanent) | Lives on epic branches (ephemeral) |
|---|---|
| `.claude/skills/`, `CLAUDE.md`, `prompts/` | `domains/<name>/` — domain plugins |
| Framework code in `packages/` | Domain-specific routes, UI pages |
| Shared utilities in `apps/api/src/` | `data/browser-profiles/<domain>/` |

**The invariant:** after an epic PR merges, delete the epic branch — nothing of lasting value is lost. Everything that matters is on `main`.

## Epic Branch Cadence

- Each epic starts from updated project `main` after the previous epic PR has merged.
- Each epic gets a branch named `epic/<epic-id>-<short-slug>`.
- Each completed epic gets exactly one PR into the project-owned base branch.
- The next epic does not begin until the previous epic PR is merged and local `main` is updated.
- If the active Beans epic and current branch name do not match, stop and correct the branch state before continuing.

**Code comments guard implementations. Skills teach generalized principles.** If a fix lives in a specific file, put the guard in the code as a comment. Skills teach HOW (generalized); prompts teach WHAT (domain-specific). Skills must be domain-agnostic.
