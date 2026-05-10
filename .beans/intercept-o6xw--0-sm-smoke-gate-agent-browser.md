---
# intercept-o6xw
title: '0-Sm: Smoke gate (agent-browser)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:24:40Z
updated_at: 2026-05-09T19:41:17Z
parent: intercept-3fqo
blocked_by:
    - intercept-aihq
---

Final epic gate. Epic E0 (intercept-3fqo) does NOT close until this passes.

Prerequisites: `docker compose up -d`, `pnpm --filter @interceptor/db migrate`, `pnpm --filter @interceptor/api dev` running on :3001.

- [x] `agent-browser open http://localhost:3001/health` loads
- [x] `agent-browser eval 'JSON.parse(document.body.innerText).status'` returns `'ok'`
- [x] `agent-browser screenshot data/smoke/phase-0-health.png`
- [x] Stop the api server; confirm `agent-browser open http://localhost:3001/health` fails (proves the route is real, not cached) — got `Navigation failed: net::ERR_CONNECTION_REFUSED`
- [x] Restart api; pass again
- [x] Bonus: `agent-browser open http://localhost:3001/api/ufcstats/events/upcoming` still works post-DB-wiring — `events.length === 9`
- [x] `agent-browser close --all`
- [x] Commit screenshot — `data/smoke/phase-0-health.png`; `.gitignore` updated from `/data/` to `/data/*` + `!/data/smoke/` so smoke evidence is tracked while runtime data stays ignored
- [x] Mark epic E0 (intercept-3fqo) completed

## Summary of Changes

Real browser drove `localhost:3001/health` end-to-end against an agent-spawned API server, confirmed `{"status":"ok"}`, captured the screenshot. Took the server down → re-ran `agent-browser open` → got `ERR_CONNECTION_REFUSED` (confirms the page isn't being served from cache). Restarted → passed again. Existing `/api/ufcstats/events/upcoming` still returns 9 events post-DB-wiring, proving Phase 0 didn't regress the existing domain proxy. Phase 0 epic intercept-3fqo can be closed.
