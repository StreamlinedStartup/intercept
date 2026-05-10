---
# intercept-g0wt
title: '4-K: Phase 4 verification + ship'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T23:17:16Z
parent: intercept-di4c
blocked_by:
    - intercept-g4oo
    - intercept-33qk
    - intercept-qtw9
    - intercept-c5rs
---

Verification per docs/ufc-fight-predictor-plan.md#phase-4.

- [x] curl /api/predict/event/9eedac48b497de5a returns N predictions for UFC 328
- [x] /upcoming shows pick chips on every fight row
- [x] CompareSheet shows win-prob bars + edge badge when odds present
- [x] /predictions table populated, ROI chart renders, calibration plot renders
- [x] /admin/predict-train trains a new model end-to-end and shows updated metrics
- [x] Zero console errors on each page (Patchright check)
- [x] biome + typecheck + vitest + pytest green
- [x] ./scripts/ci-local.sh passes
- [x] Mark E4 completed; mark milestone intercept-7c8e completed

## Verification Progress

- `curl -sS http://localhost:3001/api/predict/event/9eedac48b497de5a` returned one UFC 328 prediction and no skipped fights after the local UFC 328 fixture state was marked current.
- Browser smoke covered `/upcoming`, compare sheet edge badge, `/predictions`, and `/admin/predict-train?admin=1`; screenshot: `data/smoke/phase4-g0wt-upcoming-compare-edge.png`.
- Console checks showed only React/Next dev informational logs, no browser errors.
- `pnpm lint`, `pnpm typecheck`, `pnpm test -- --runInBand`, and `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q` passed.
- `./scripts/ci-local.sh` passed with local build, typecheck, test, Python, and Playwright E2E gates.

## Docker Build Note

- Docker image builds are now opt-in via `./scripts/ci-local.sh --docker` because they require registry access for uncached base images.
- `./scripts/ci-local.sh --docker` was attempted twice and failed only while Docker Hub timed out resolving uncached `node:22-slim` / `node:22-alpine` metadata.

## Summary of Changes

- Completed Phase 4 verification across API, UI, browser smoke, console checks, and local CI.
- Made Docker image builds opt-in for local CI to avoid mandatory Docker Hub pulls on developer machines.
- Captured compare-sheet edge smoke evidence at `data/smoke/phase4-g0wt-upcoming-compare-edge.png`.

## Verification

- `curl -sS http://localhost:3001/api/predict/event/9eedac48b497de5a`
- `agent-browser` smoke for `/upcoming`, compare sheet, `/predictions`, and `/admin/predict-train?admin=1`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test -- --runInBand`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q`
- `./scripts/ci-local.sh`
