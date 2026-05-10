---
# intercept-g7uh
title: '1-C: UI badge on event-fight-card showing state + Load button'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T20:23:28Z
parent: intercept-1shv
blocked_by:
    - intercept-mlyq
---

User-visible affordance. Single fighter at a time still — no batching, no bulk, no fancy worker.

- [x] event-fight-card.tsx: for each fighter cell, fetch /api/predict/backfill/state/:id; render colored dot (red none, green current)
- [x] If state=none, render 'Load' button next to the name; click → POST backfill then re-fetch state
- [x] Spinner while POST is in-flight (button stays inline, disabled)
- [x] Test on UFC 328 main event: red dots → click Load → green dots within ~10s

## Summary of Changes

Added per-fighter backfill state loading to the upcoming fight card. Fighter cells now render status dots, show inline Load buttons only for `none`, disable the button with a spinner during POST, then refetch state after the synchronous backfill completes.

Verification:
- pnpm --filter @interceptor/web typecheck
- agent-browser open http://localhost:3000/upcoming
- agent-browser snapshot showed Load buttons on `none` fighters and UFC 328: Chimaev vs. Strickland on the page
- agent-browser click on the UFC 328 main-event Load button disabled the button during POST, then removed it after state became current
- agent-browser snapshot showed Khamzat Chimaev image current and Sean Strickland image current; current/none dot count was current=2, none=50
