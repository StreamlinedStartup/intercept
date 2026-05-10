# Workflow Rules

- Never `git add -A` — stage specific files by name
- Always run `./scripts/ci-local.sh` before committing
- Track multi-attempt difficulties: 5+ approaches = document the problem
- **Do not retry on unexpected output.** If a request returns HTML instead of JSON, a 429, or an empty response — that IS the answer. Investigate the response (check content-type, status code, response body). Do not retry the same request with minor tweaks (different headers, sleep between). Retrying wastes tool calls and never works.
- **One install, one server start.** Run `pnpm install` once. If it fails, fix the error — do not retry with different flags. Start the API server once. If the port is in use, kill it once with `lsof -ti:PORT | xargs kill 2>/dev/null`, then start. Do not loop.

## Epic Branch Cadence

- One epic gets one branch and one PR. Never continue a new epic on a previous epic's branch.
- Before starting an epic, run `beans list --ready` and `beans show <epic-id>`, then verify the branch name matches that epic.
- Branch format: `epic/<epic-id>-<short-slug>`.
- New epic branches start from the project-owned base branch after the previous epic PR has merged.
- If the current branch name belongs to an older epic, stop feature work and fix the branch/PR state before writing code.
- Complete each child bean with its own commit. Complete the epic only after all children, verification, and smoke gate are committed.
- When an epic is confirmed complete, push the epic branch, open exactly one PR for that epic, merge it into the project base branch, switch back to the base branch, update it from the project remote, then create the next epic branch.
- Do not reuse merged epic branches. Do not stack multiple epics on one branch.

## Process Cleanup

Clean up everything you started before finishing or switching context:

```bash
pkill -f "connect-browser"              # Browser sessions
pkill -f "tsx.*src/index"               # tsx watchers
lsof -ti:3001 | xargs kill 2>/dev/null  # API server
lsof -ti:3000 | xargs kill 2>/dev/null  # Web server
```

## Test → Base Flow

On test branches, NEVER edit CLAUDE.md or `.claude/skills/` directly. Write to the fix queue:

```
~/.claude/projects/<project-hash>/memory/base-fixes-needed.md
```

On return to `base`: read, apply, clear, run CI, commit.
