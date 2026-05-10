---
# intercept-a5wm
title: '4-B: Prediction chip on /upcoming fight rows (visual slice closes)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:07:48Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

User-visible: every fight row shows the model's pick.

- [x] event-fight-card.tsx: for each fight row, fetch /api/predict/fight/:id when both fighters are state='current'
- [x] Render a small chip after the weight-class badge: '58% Khamzat ✓' style
- [x] If either fighter not loaded: 'Backfill required' chip (greyed out)
- [x] Test on UFC 328 main event after backfilling Khamzat + Strickland

## Summary of Changes

- Added prediction state to `/upcoming` fight cards so rows with two `current` fighters call `GET /api/predict/fight/:id`.
- Rendered prediction chips after weight-class badges, including model pick/probability, loading, unavailable, and `Backfill required` states.
- Mirrored the API's pending fight-id derivation so upcoming fights without official UFCStats fight IDs can still resolve seeded DB rows.

Verified:

- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check apps/web/src/app/'(dashboard)'/upcoming/event-fight-card.tsx`
- `agent-browser snapshot` on `http://localhost:3000/upcoming` showed the current live main event chip as `68% Arnold Allen` and unloaded rows as `Backfill required`.
- `agent-browser screenshot data/smoke/phase4-a5wm-prediction-chip.png`
- The original UFC 328/Khamzat verification target is no longer in the `/upcoming` seven-day window on 2026-05-10, so the same behavior was verified against the current live card, `UFC Fight Night: Allen vs. Costa`.
