---
# intercept-5cmh
title: '1-Sm: Smoke gate (agent-browser)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:24:40Z
updated_at: 2026-05-09T22:17:25Z
parent: intercept-1shv
blocked_by:
    - intercept-bgxt
---

Final epic gate. Epic E1 (intercept-1shv) does NOT close until this passes.

Prerequisites: api + web running. /upcoming reachable. DB seeded with current events from ufcstats route cache.

- [x] `agent-browser open http://localhost:3000/upcoming` loads cleanly
- [x] `agent-browser screenshot data/smoke/phase-1-initial.png` shows mixed live DB states, including red Load badges and green loaded dots
- [x] `agent-browser snapshot` confirms backfill controls are present in the accessibility tree
- [x] Click Load on an unloaded upcoming fighter; live card updated to green
- [x] `agent-browser screenshot data/smoke/phase-1-loaded.png` shows green loaded badges after the browser-triggered load
- [x] Open compare sheet; `agent-browser screenshot data/smoke/phase-1-compare-state.png` confirms both corner cells render Loaded state
- [x] /admin/predict-train?admin=1: click 'Seed: in-window' -> progress/metrics appear; `agent-browser screenshot data/smoke/phase-1-seed.png`
- [x] `agent-browser eval 'window.__errors || []'` returned `[]`
- [x] `agent-browser close --all`
- [x] Commit screenshots
- [x] Mark epic E1 (intercept-1shv) completed

## Summary of Changes

Ran the required Phase 1 browser smoke gate against the local API, web app, and
Postgres database. The live local DB was already partially seeded, so the smoke
used actual mixed states instead of a pristine all-red initial state. The
screenshots are committed under `data/smoke/`.

Evidence:

- `agent-browser open http://localhost:3000/upcoming` loaded the Upcoming Fights page.
- `agent-browser snapshot -i` showed compare buttons plus Load controls for unloaded fighters.
- `data/smoke/phase-1-initial.png` captures the mixed initial state.
- Browser click on an unloaded fighter completed and `data/smoke/phase-1-loaded.png` shows additional green loaded state.
- `data/smoke/phase-1-compare-state.png` captures Loaded badges in the compare sheet corner cells.
- `data/smoke/phase-1-seed.png` captures the admin seed result after clicking Seed: in-window.
- `agent-browser eval 'window.__errors || []'` returned `[]`.
- `agent-browser close --all` completed.
- API and web dev servers were stopped after the smoke.
