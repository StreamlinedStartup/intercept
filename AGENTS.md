# Project Guide for Coding Agents

> **This file is mirrored to `AGENTS.md`.** Keep them identical — they exist so the same instructions work across Claude Code, Cursor, Codex CLI, and any other harness that reads agent instructions from a project-root file. If you edit one, edit the other (or run `cp CLAUDE.md AGENTS.md`).

## What this project is

Two things, sharing one repo:

1. **Interceptor** — a TypeScript framework for discovering a website's internal API via browser traffic interception, then exposing that API as typed proxy routes. Each target site becomes a "domain plugin" under `domains/<name>/`. The framework is mature (browser auto-start, traffic capture, transport classifier, GenericSessionManager, rate limiter, file cache). See `.claude/rules/discovery.md` for the discovery protocol; `domains/boardshop/` is the reference plugin with examples of every transport type.

2. **UFC Fight Predictor** — a product built on top of Interceptor. Scrapes ufcstats.com (the `domains/ufcstats/` plugin), pulls moneyline odds from `the-odds-api.com` (the `domains/odds-mma/` plugin, in progress), trains an XGBoost model in Python on historical fights, and surfaces predictions inline in the Next.js dashboard at `/upcoming` plus a `/predictions` track-record page.

If you're picking up work mid-stream, **read `~/.claude/plans/the-odds-api-is-cuddly-dewdrop.md`** — it's the approved implementation plan for the Predictor work and is the source of truth for the database schema, the on-demand backfill model, the feature engineering, and the metric targets.

## Current status (2026-05-09)

| Piece | State |
|---|---|
| Interceptor framework | Complete + working |
| `domains/boardshop` reference plugin | Complete |
| `domains/ufcstats` (HTML scraper, 6 routes, file cache) | Complete |
| `/upcoming` dashboard (event cards + matchup compare sheet) | Complete |
| `packages/db` (Postgres + TimescaleDB + Drizzle) | **In progress — Phase 0** |
| On-demand fighter backfill | Not started — Phase 1 |
| `domains/odds-mma` plugin | Not started — Phase 2 |
| Python XGBoost training + inference | Not started — Phase 3 |
| Predictions UI + admin retrain | Not started — Phase 4 |

## Workspace layout

```
apps/
├── api/                   Hono API server (port 3001), WebSocket browser stream, domain proxy routing
└── web/                   Next.js 16 dashboard (port 3000), shadcn/ui, dark theme

packages/
├── browser/               Patchright browser automation + transport classifier
├── shared/                rateLimitedFetch, DEBUG, validation, Python IPC bridge
├── test-server/           Fake sites on port 4444 for validating new discoveries
└── db/                    NEW (Phase 0) — Drizzle ORM + Postgres/TimescaleDB

domains/
├── boardshop/             Reference plugin — every transport type covered
├── ufcstats/              UFC fight stats scraper (6 routes + file cache)
└── odds-mma/              NEW (Phase 2) — the-odds-api.com moneyline odds

services/
└── python/                JSON-RPC worker over stdio. Will host XGBoost training + inference (Phase 3)

data/
├── browser-profiles/      Persisted Patchright profiles per domain
├── fixtures/              Cached JSON responses for UI iteration without live calls
└── cache/                 File cache used by ufcstats domain (per-bucket TTL)
```

## Quick commands

```bash
pnpm dev                                       # All services (API 3001, Web 3000)
pnpm --filter @interceptor/api dev             # API only
pnpm --filter @interceptor/web dev             # Web only
pnpm --filter @interceptor/test-server start   # Mock sites on 4444
pnpm --filter @interceptor/api typecheck       # tsc --noEmit
pnpm biome check --write .                     # Lint + format (auto-fix)
./scripts/ci-local.sh                          # Full CI — run before committing

# Predictor pipeline (when implemented)
docker compose up -d                           # Postgres + Timescale
pnpm --filter @interceptor/db migrate          # Apply schema + create_hypertable
pnpm --filter @interceptor/api train           # Triggers Python ml.train via IPC
```

## Architecture cheatsheet

- **Domain proxy:** any plugin route at `/api/<domain>/<path>`. Plugin registered in `apps/api/src/register-domains.ts`.
- **Domain shape:** `domains/<name>/src/{index,config,interceptor,routes,cache}.ts`. Use `bash .claude/skills/api-discovery/scripts/scaffold-domain.sh <name> <root-domain>` to scaffold.
- **Routes:** export `DomainRoute[]` from `routes.ts`. `browserRequired: false` for pure-HTTP routes (most cases). Use `rateLimitedFetch` first; only escalate to `browserFetch` if direct HTTP is blocked.
- **Cache:** file-based JSON cache pattern in `domains/ufcstats/src/cache.ts` — copy this for new domains. Per-bucket TTL, `?refresh=1` bypass, `X-Cache: HIT|MISS|BYPASS|SKIP` header, matching `Cache-Control: public, max-age=<seconds>`.
- **Rate limit:** `registerRateLimit('hostname', { maxPerMinute, retryOn429 })` in `register-domains.ts`. Default 30/min for polite sites; tighter for paid APIs.
- **Browser WebSocket:** `ws://localhost:3001/browser/stream?profile=<domain>&url=<target>` — only for discovery / sites that block direct HTTP.
- **Traffic capture:** `GET /browser/traffic` — only WS-connected browsers capture.
- **Debug logs (Node):** `import { DEBUG } from '@interceptor/shared'` → `/tmp/interceptor-debug/`.
- **Debug logs (browser/web):** `import { DEBUG } from '@/lib/debug'` — same API but no Node-only deps.
- **Frontend API URLs:** relative (`/api/...`), never `http://localhost:3001/...`. Next.js rewrites proxy through.

## Database (in progress — Phase 0)

- Postgres 16 + TimescaleDB extension via `docker-compose.yml`.
- Drizzle ORM in `packages/db/`. Schema in `packages/db/src/schema.ts`.
- 9 tables (see plan file): `events`, `fighters`, `fighter_backfill_state`, `fighter_stat_snapshots` (hypertable), `fights`, `fight_results`, `fight_round_stats`, `odds_snapshots` (hypertable), `predictions` (hypertable), `model_versions`.
- TimescaleDB hypertables created in a post-migration step (`packages/db/src/migrate.ts`) since Drizzle migrations don't model `create_hypertable()`.
- `DATABASE_URL` env var. App should fail loud at startup if missing — never silently work without DB.

## Predictor pipeline (planned)

- **Backfill:** on-demand per fighter, triggered from the `/upcoming` UI. Per-fighter status: `none|current|stale_count|stale_stats|in_progress|failed`. Background worker is in-process; jobs disappear on crash and the UI retries. Admin "Seed" buttons bulk-queue fighters from recent UFC events to bootstrap the training set.
- **Odds:** `domains/odds-mma/` proxies the-odds-api.com (free tier: 500/mo, 5/min). Daily cron snapshots into `odds_snapshots`. Fuzzy-matches fighter names to our DB; unmatched rows go to `unmatched_odds` for review, never silently dropped.
- **Training:** Python service via existing JSON-RPC bridge (`packages/shared/src/python-bridge/`). Chronological 80/20 split (no random — would leak future). XGBoost native NaN handling. Metrics: log loss, Brier score, accuracy, ROC AUC, ROI vs market. Saved to `data/models/` + row in `model_versions`.
- **Features:** see plan file for the full list. Includes statistical differentials, physicals (height/reach/age), stance interaction (orthodox vs southpaw is asymmetric — keep direction), UFC-specific experience, recent form (rolling windows), weight-class change detection, damage proxy.
- **Predictions UI:** chip on each fight row in `/upcoming`, win-prob bars in compare sheet, full track record + calibration plot at `/predictions`, admin retrain at `/admin/predict-train`.

## Task tracking — Beans is mandatory

**All work — every epic, feature, task, bug — lives in `beans` (CLI: `beans`). No exceptions.**

- Do **not** use ad-hoc TODO lists, in-chat task trackers (TodoWrite, etc.), or scratch markdown for work tracking. Use beans.
- Issue types: `milestone` (release / phase target) → `epic` (thematic container) → `feature` / `task` / `bug`.
- Every multi-step piece of work gets a parent epic + child tasks with explicit `--blocked-by` dependencies. The dependency graph IS the plan.
- Run `beans list --ready` to see what's actually unblocked. Don't pick work outside that list.
- Body content is the source of truth for acceptance criteria. Keep `- [ ]` checkboxes current as you make progress (`- [ ] x` → `- [x] x`).
- When completing a bean, append a `## Summary of Changes` section. When scrapping, append `## Reasons for Scrapping`.
- Commit beans alongside code changes — they're markdown files in `.beans/`, version-controlled.

Common commands (use `--json` when parsing programmatically):

```bash
beans list --ready                                        # what's unblocked right now
beans list -S "ufc"                                       # full-text search
beans show <id>                                           # full body + relationships
beans create "Title" -t epic -d "..." -p high            # new epic
beans create "Title" -t task --parent <epic-id> --blocked-by <other> -s todo
beans update <id> -s in-progress
beans update <id> -s completed --body-replace-old "- [ ] X" --body-replace-new "- [x] X"
```

**Before starting any phase: graph every epic + task + dependency in beans first.** No code work begins until the graph for that phase exists and is approved.

## Git workflow — non-negotiable

**Every completed bean task gets its own commit. Every completed epic gets its own PR. No exceptions.**

### Remote boundary — never submit upstream to original Interceptor

**This repo is now a separate UFC Fight Predictor product. It must never submit work upstream to the original `intercept` project. No exceptions.**

- Do not open pull requests against `adam-s/intercept` or any other original/upstream Interceptor repository.
- Do not push branches to an upstream Interceptor remote, even if credentials appear to allow it.
- Do not fork upstream Interceptor for contribution purposes, and do not create cross-repo PRs targeting upstream Interceptor.
- Do not merge, squash, rebase, or otherwise land this project’s work into upstream Interceptor.
- Treat any remote named `origin` or `upstream` that points at original Interceptor as read-only historical context only.
- If a PR is required for an epic, create it only inside this project’s own GitHub repository/fork. If that remote does not exist, create a new project-owned remote and use that as the destination.
- If the user asks to “push remote,” “open PR,” or “merge PR,” first verify the destination is not upstream Interceptor. Refuse and explain if the only available destination is upstream Interceptor.

- Do not batch multiple completed tasks into one commit unless a bean explicitly defines them as one task.
- Do not close a bean until its code/docs/fixtures, bean file update, and verification evidence are committed together.
- Do not close an epic until every child task is committed, the smoke gate is committed, and a PR exists for the epic.
- Commit immediately after each task passes its verification gate. If verification is blocked, commit only when the bean clearly records the blocker and the user explicitly approves the partial commit.
- PR scope is exactly one epic. If another epic's work is needed, open a separate PR or split the beans first.
- Stage files explicitly by path. Never use `git add -A`.
- Commit generated evidence that proves the task when required: smoke screenshots, fixture updates, migrations, and bean markdown.
- Keep commit and PR text token-aware: concise, evidence-first, no narrative filler, no pasted logs unless a short excerpt is the evidence.

### Commit template

Subject:

```text
<bean-id>: <imperative summary>
```

Body:

```text
Why:
- <1 bullet, only if context is not obvious>

Changed:
- <high-signal change>
- <high-signal change>

Verified:
- <command or smoke evidence>
- <command or smoke evidence>
```

Rules:

- Subject should stay under ~72 chars when practical.
- Omit `Why` if the subject and bean title make the reason obvious.
- Use 1-3 bullets per section. Prefer file/route names over prose.
- Mention known gaps only when they matter for the next bean.

Example:

```text
intercept-vuac: add synchronous fighter backfill route

Changed:
- Added POST /api/predict/backfill/fighter/:id
- Upserted fighter, event, fight, result, and round stat rows
- Completed intercept-vuac acceptance checks

Verified:
- pnpm --filter @interceptor/api typecheck
- SELECT count(*) FROM fight_results WHERE fighter_id='767755fd74662dbf' => 10
```

### PR template

Title:

```text
<epic-id>: <epic title>
```

Body:

```text
## Scope
- <what this epic ships>
- <what is intentionally out of scope, if useful>

## Beans
- <epic-id>
- <task-id>: <short title>
- <task-id>: <short title>

## Verification
- <CI command or focused checks>
- <agent-browser smoke screenshot path, if required>

## Risk
- <main risk or "Low: <reason>">
```

Rules:

- Keep the PR body short enough to review quickly. Link to beans for detail instead of repeating every acceptance criterion.
- Include the smoke screenshot path for HTTP/UI epics.
- Include migrations, env changes, and operator steps only when the reviewer must act on them.

### Smoke gate — every epic with HTTP or UI must pass `agent-browser`

Every epic that ships an HTTP endpoint or UI surface gets a final task `<phase>-Sm: agent-browser smoke gate`. **The epic cannot be marked completed until that smoke passes.** No exceptions.

- The smoke task is `--blocked-by` the epic's verification task (`<phase>-J` or equivalent) and is the LAST work item in the epic.
- The next phase's first task depends on this smoke gate, not on internal verification — i.e. Phase N's first task is `--blocked-by` Phase N-1's smoke gate.
- The CLI is `agent-browser` (`/opt/homebrew/bin/agent-browser`, v0.27.0+). Use it directly — do NOT substitute curl/Patchright scripts and call it "good enough." The point is to drive a real browser the way a user would.
- Screenshots produced by the smoke gate go to `data/smoke/<phase>-<short-name>.png` and are committed alongside the epic close.
- A smoke gate that "passes locally on my machine" without a screenshot artifact does not count. Evidence is required.

Skeleton commands every smoke gate uses:

```bash
agent-browser open http://localhost:3000/<route>
agent-browser screenshot data/smoke/<phase>-<name>.png
agent-browser snapshot                                    # accessibility tree (read by you to verify content)
agent-browser click 'button:has-text("X")'
agent-browser eval 'JSON.parse(document.body.innerText)'  # for JSON endpoints
agent-browser close --all                                 # cleanup
```

Pure backend epics (no HTTP, no UI — e.g. a pure Python module change) are exempt; verify via `pytest` only.

## Methodology — Thin / Vertical Slice + KISS

- **Vertical slice over horizontal layer.** Each task should slice through every layer (DB → API → UI) for ONE small piece of working functionality, end to end. **Do not** build all DB tables, then all routes, then all UI components. Build the smallest thing that works top-to-bottom, prove it, then build the next slice.
- **Definition of "thin":** the slice is shippable on its own. A user can use the feature, even if the feature is tiny. "Backfill one fighter and see a green badge" is thinner than "build all backfill state machinery, then all UI." Choose thinner.
- **KISS — Keep It Simple, Stupid.** Default to the simplest thing that works. No premature abstraction. No "we might need this later." No defensive cruft for hypothetical futures. Three similar lines beat a premature abstraction. Delete code that isn't used.
- **No over-design.** A `Map<jobId, JobState>` in memory beats a job queue library, until proven otherwise. A single Hono route file beats a routes/services/controllers split, until the file actually gets unwieldy. Earn complexity; don't budget for it.
- **Failure surfaces immediately.** No silent fallbacks. If the DB is down, fail loud at startup. If a fetch returns 503, return the 503 — don't paper over with a "default" response.

## Conventions

- **TypeScript strict.** No `any` unless justified (cheerio dynamic types are the existing exception).
- **Biome for lint/format.** Run `pnpm biome check --write .` before committing — manual fixes only after auto-fix.
- **Tests.** Vitest co-located (`foo.ts` → `foo.test.ts`); integration tests in `tests/`. Pytest for Python.
- **CI gate.** `./scripts/ci-local.sh` must pass: install (frozen lockfile), biome, build, typecheck, vitest, pytest. Run before every commit.
- **Imports.** `@interceptor/<package>` for workspace, `@/...` for app-internal aliases.
- **Frontend fetches.** Always relative URLs.
- **No emojis.** In code, comments, commits, or docs unless the user explicitly asks. (UI labels showing user-visible emoji like ⚡ for "live" are fine.)
- **No fallback mechanisms** — they hide real failures. Surface errors with actionable messages.
- **No `git add -A`.** Stage specific files by name to avoid grabbing secrets or build output.
- **Comments.** WHY-only when non-obvious. Don't restate the code.

## Operating principles

- **Code ownership.** We own everything — apps, packages, domains, scripts, infra. When something is broken, fix it at the source. No workarounds, no "document for later", no dummy values to satisfy a type. If an interface is wrong, fix the interface. Breaking changes are fine — pre-release.
- **Cleanup.** Always kill background processes you started before finishing a task: `lsof -ti:3000 | xargs kill -9`, `pkill -f "tsx.*src/index"`, etc.
- **One install, one server start.** `pnpm install` once. If it fails, fix the error. Start the API server once. If the port is in use, kill it once with `lsof -ti:PORT | xargs kill 2>/dev/null`. Don't loop.
- **Unexpected output is information.** A 429 IS the answer. Don't retry the same request with minor tweaks — investigate. (See `.claude/rules/workflow.md`.)
- **Verification gates.** A feature isn't done until you have evidence: curl output, screenshot, passing test. Trust but verify.

## Worktree mode

If `pwd` contains `/tmp/interceptor-worktrees/`, you are in an isolated worktree:
- All files go in YOUR worktree. Never write to the original repo.
- The API server does NOT auto-reload domain file changes. Edit → `kill -9` server → restart.
- After domain edits, update `register-domains.ts` in YOUR worktree to import the plugin.
- Test through `localhost:PORT/api/<domain>/<route>`.

## Skill / sub-agent integration

- `.claude/skills/api-discovery/` — full discovery protocol (PRE-FLIGHT → GATHER → SCAN → CLASSIFY → BUILD).
- `.claude/skills/dashboard-builder/` — Next.js dashboard patterns + shadcn/ui catalog.
- `.claude/skills/visual-dev/` — Patchright screenshot loop for UI iteration.
- `.claude/skills/debug-logs/` — iterative log-driven debugging.
- `.claude/skills/systematic-testing/` — bottom-up validation across architecture layers.
- `.claude/rules/` — committed protocols (discovery, prompt-compliance, workflow, base-branch).
- `.claude/agents/` — sub-agent definitions for parallel exploration / review.

These are read by Claude Code's skill system. Other harnesses can read them as plain markdown but won't auto-invoke; reference them explicitly when needed.

## Pointers

- **Active plan:** `docs/ufc-fight-predictor-plan.md` — UFC Fight Predictor implementation, phases 0-4.
- **Live work graph:** `beans list` (full tree), `beans list --ready` (unblocked work). Roadmap snapshot: `docs/roadmap.md` (regenerate with `beans roadmap > docs/roadmap.md`).
- **Reference domain:** `domains/boardshop/src/routes.ts` — every transport type with a working example.
- **Working domain:** `domains/ufcstats/src/{routes,cache}.ts` — pattern for a pure-HTTP scraper plugin.
- **Discovery rules:** `.claude/rules/discovery.md` (mandatory protocol before writing routes for a new site).
- **Prompt compliance:** `.claude/rules/prompt-compliance.md` (matrix-style verification before commits).

## Communication

- Be concise. Match response length to question complexity.
- State results and decisions directly. Don't narrate internal deliberation.
- Use `file_path:line_number` when pointing at code.
- One- to two-sentence end-of-turn summaries: what changed + what's next.
- Never claim a task is done until you have evidence (curl output, screenshot, green test). Saying "should work" doesn't count.


<claude-mem-context>
# Memory Context

# [intercept] recent context, 2026-05-09 5:10pm MST

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (19,490t read) | 1,952,930t work | 99% savings

### May 9, 2026
S527 UFC Fight Predictor v1 project bootstrap complete; agent-browser CLI confirmed available for ufcstats.com API discovery (May 9 at 11:31 AM)
1919 11:59a 🟣 Phase 4 Predict API + UI task graph completed — full 46-task beans graph verified
1921 12:16p 🔴 Cross-phase blocking dependencies added — beans list --ready now enforces sequential phase execution
S529 UFC Fight Predictor v1 full bootstrap complete — beans graph finalized with smoke gates, context handoff prompt generated for next session (May 9 at 12:16 PM)
S525 Bootstrap /Users/vulturestudio/intercept UFC Fight Predictor v1 project with beans task graph and coding agent documentation (May 9 at 12:16 PM)
S526 UFC Fight Predictor v1 project bootstrap complete — beginning Phase 0 implementation with agent-browser discovery (May 9 at 12:16 PM)
1922 12:22p ⚖️ agent-browser smoke gate policy added to CLAUDE.md
1923 12:24p 🟣 Smoke gate beans created for Phases 0, 1, 2, and 4
1924 12:25p 🔵 beans update supports explicit edge removal via --remove-blocked-by and --remove-blocking
1925 " ✅ Cross-phase blocking chain rewired through smoke gate tasks
1926 " ✅ Final beans graph state: 56 beans, 50 tasks, 4 smoke gates, roadmap regenerated
S530 UFC Fight Predictor Phase 0 infra: completed tasks intercept-tmtz (Postgres+TimescaleDB), intercept-dvmr (@interceptor/db skeleton), and intercept-dwtm (events+fighters schema + first migration) (May 9 at 12:25 PM)
S528 UFC Fight Predictor v1 beans graph finalized with agent-browser smoke gates; all cross-phase dependencies rewired; ready to begin Phase 0 implementation (May 9 at 12:25 PM)
1927 12:27p 🔵 UFC Fight Predictor Project Session Resumed in /intercept
S531 UFC Fight Predictor Phase 0 — Postgres/TimescaleDB/Drizzle infra + API DB wiring + smoke gate (completed full epic) (May 9 at 12:32 PM)
1928 12:33p 🟣 Drizzle Schema for events + fighters Completed with First Migration
1929 " 🟣 @interceptor/db Client Singleton and Migration Runner Created
1930 " 🟣 Migration Applied to Live TimescaleDB — events and fighters Tables Confirmed
1931 12:34p 🟣 Phase 0 End-to-End Smoke Script Created
1932 " 🟣 Phase 0 Vertical Slice Proven — Smoke Test Passes End-to-End
1933 " ✅ @interceptor/db README Documents Hypertable Architecture Constraint
1934 " 🔵 Phase 0-E Completion Unblocks Two Parallel Tasks: 0-F and 0-H
1935 12:35p 🔵 Phase 0 Remaining Schema Tables Specified — 7 Tables for Task 0-F
1936 " 🟣 Full Database Schema Written — All 9 Tables Defined in schema.ts
1937 " 🟣 Second Migration Generated and Applied — All 10 Tables Now Live in Database
1939 " 🟣 Smoke Script Extended to Round-Trip All 10 Tables
1938 12:36p 🔵 All 10 Tables Confirmed Present in Live interceptor-postgres Container
1940 " 🟣 Full 10-Table Smoke Test Passes — Phase 0-F Complete
1941 " 🔵 Drizzle Composite PK Deprecation Warning Deferred — TS6387 extraConfig Callback Form
1942 12:37p 🔵 Task 0-G: TimescaleDB Hypertable Conversion Pattern Specified
1943 " 🟣 TimescaleDB Hypertables Created via Post-Migration Hook in migrate.ts
1944 " 🔵 Hypertables Confirmed Active and migrate.ts Idempotency Verified
1945 " 🔵 migrate_data => TRUE Required When Hypertable Table Already Has Rows
1946 12:38p 🔵 apps/api Existing Structure Examined Before DATABASE_URL Wiring
1947 " ✅ @interceptor/db Added as Workspace Dependency to apps/api
S532 Resume UFC Fight Predictor — Phase 0 commit prep, schema cleanup (varchar→text), migration, and CI verification before proceeding to Phase 1/2 (May 9 at 12:38 PM)
S533 Phase 0 schema cleanup: varchar→text migration + full clean-install verification on fresh DB (May 9 at 12:43 PM)
S534 Phase 0 schema fix fully verified: varchar→text migration confirmed clean on fresh DB, bean 0-G updated to reflect deferred warning now resolved (May 9 at 12:50 PM)
1948 4:41p ⚖️ Intercept Fork: Upstream PR Ban and Workflow Constraints Established
1949 4:42p 🔵 CLAUDE.md and AGENTS.md Are Not Byte-Identical — Constraint Violation
1950 " 🔵 Phase 2 Odds-MMA Plugin Fully Implemented — Only Verification Bean Remains
1951 " 🔵 Local Branch and Fork/Main Have Diverged — Squash vs Detailed History
1952 " 🔵 Ready Beans at Session Start: Phase 2 Verification and Phase 3 Python Setup
1953 " 🔵 cp CLAUDE.md AGENTS.md Silently Fails — AGENTS.md Remains 32 KB Despite Copy
1962 " ⚖️ Intercept Fork: Upstream PR Submission Permanently Banned
1955 4:52p 🔵 Phase 2 odds-mma domain plugin: full route and env var map
1956 " 🔵 Bean intercept-1fhe verification commands and test targets mapped
1957 " 🔵 DB schema for odds-mma: odds_snapshots and unmatched_odds tables
1958 " 🔵 Files to stage if only bean status or summary changes in intercept-1fhe
1954 4:53p 🔵 UFC Fight Predictor Beads Task Queue State
1959 4:54p 🔵 Intercept Project Phase Completion Status — Phases 0–2 Done, Phase 3 Next
1960 " 🔵 Intercept Monorepo Structure with Existing Python Service Directory
1961 " 🟣 Sub-agent "Jason" Spawned to Implement Bean 3-A: Python DB Plumbing
**1963** 4:58p 🔵 **CLAUDE.md and AGENTS.md Diverged: AGENTS.md Had Extra Trailing Content**
At session start, the required byte-identity invariant between CLAUDE.md and AGENTS.md was violated. AGENTS.md had grown to 32183 bytes (vs CLAUDE.md at 20733) due to trailing blank lines added by commit f657b6f. The fix is simple — cp CLAUDE.md AGENTS.md — but the first cp attempt during the session also showed DIFFER because cmp was run before the file was flushed (or because CLAUDE.md itself had unstaged modifications). The second cp at session end confirmed IDENTICAL. Future agents must always verify with cmp after any edit to either file.
~325t 🔍 176,477

**1964** " 🔵 **Phase 2 Odds-MMA Implementation Already Shipped in fork/main**
The session discovered that the fork's squash merge had already included Phase 2 implementation work. The local detailed commit history on epic/phase-1-backfill-pr contains individual commits for each Phase 2 task, but the fork's main is a squash. The remaining Phase 2 work was purely verification and smoke gate beans, not new implementation. This means the session could skip straight to running the API and proving the endpoints work.
~335t 🔍 176,477

**1965** " 🔵 **API Server Binds IPv6-Only: curl to 127.0.0.1:3001 Fails Without Elevated Permissions**
The Hono API server, started with tsx, binds to IPv6 wildcard (*:3001) on macOS. Claude Code's sandbox blocks loopback TCP connections by default. Two workarounds were used: (1) adding sandbox_permissions=require_escalated to curl commands, and (2) using agent-browser which is an external process not subject to the sandbox. This is a recurring pattern for any API verification work in this project.
~318t 🔍 176,477

**1966** " 🟣 **Phase 2 Verification Bean (intercept-1fhe) Completed**
The Phase 2 verification bean required live evidence from the running API. The 0/288 match rate for odds rows against canonical fights is expected and correct — the live-betting odds API returns upcoming fights whose dates don't align with the existing local seed data (historical results). The unmatched path is fully exercised and logged to unmatched_odds, which is the designed behavior for v1. All test/typecheck/lint gates passed.
~350t 🛠️ 176,477

**1967** " 🟣 **Phase 2 Smoke Gate (intercept-qjks) Completed with agent-browser**
The Phase 2 smoke gate verifies HTTP endpoints using agent-browser as a real browser client (since Phase 2 ships no UI). The API server needed to be restarted to get a fresh cache for the MISS/HIT cycle (the first server session had a warm cache from previous verification runs). The agent-browser workaround for the sandbox loopback restriction worked cleanly. The smoke produced the required screenshots and closed the Phase 2 epic.
~369t 🛠️ 176,477

1968 " 🟣 Phase 2 PR #2 Created at StreamlinedStartup/intercept
1969 " 🔵 Odds Matching Always Returns 0 Matches Against Local Seed Data

Access 1953k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>