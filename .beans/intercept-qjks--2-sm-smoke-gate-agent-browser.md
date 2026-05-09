---
# intercept-qjks
title: '2-Sm: Smoke gate (agent-browser)'
status: completed
type: task
created_at: 2026-05-09T19:24:40Z
updated_at: 2026-05-09T23:48:15Z
parent: intercept-8gxf
blocked_by:
    - intercept-1fhe
---

Final epic gate. Epic E2 (intercept-8gxf) does NOT close until this passes.

Phase 2 ships HTTP endpoints (no new UI). Verify via agent-browser as a real client.

Prerequisites: api running, ODDS_API_KEY set, db migrated.

- [x] `agent-browser open http://localhost:3001/api/odds-mma/upcoming`
- [x] `agent-browser eval 'JSON.parse(document.body.innerText).length'` returns > 0 (real odds)
- [x] `agent-browser screenshot data/smoke/phase-2-upcoming.png`
- [x] Reload twice -> response headers should show `X-Cache: MISS` then `HIT` (verify in DevTools network panel via `agent-browser eval` on performance entries, or check api logs)
- [x] `agent-browser open http://localhost:3001/api/odds-mma/snapshot`
- [x] `agent-browser eval 'JSON.parse(document.body.innerText).rows_written'` > 0
- [x] `agent-browser screenshot data/smoke/phase-2-snapshot.png`
- [x] psql verify: `SELECT count(*) FROM odds_snapshots WHERE snapshot_at > now() - interval '5 minutes'` > 0
- [x] `agent-browser close --all`
- [x] Commit screenshots
- [x] Mark epic E2 (intercept-8gxf) completed

## Summary of Changes

Ran the required Phase 2 browser smoke gate against the local API and TimescaleDB database. The smoke used a real browser as the HTTP client for both odds endpoints and saved the required screenshots under `data/smoke/`.

Evidence:

- `agent-browser open http://localhost:3001/api/odds-mma/upcoming`
- `agent-browser eval 'JSON.parse(document.body.innerText).length'` returned 53.
- `agent-browser screenshot data/smoke/phase-2-upcoming.png`
- Fresh-cache header checks returned `X-Cache: MISS` followed by `X-Cache: HIT`; API logs also showed `wrote bucket=oddsList` then `hit bucket=oddsList`.
- `agent-browser open http://localhost:3001/api/odds-mma/snapshot`
- `agent-browser eval 'JSON.parse(document.body.innerText).rows_written'` returned 275.
- `agent-browser screenshot data/smoke/phase-2-snapshot.png`
- `SELECT count(*) FROM odds_snapshots WHERE snapshot_at > now() - interval '5 minutes';` returned 825 after repeated smoke/verification snapshots.
- `agent-browser close --all`
