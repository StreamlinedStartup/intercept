---
# intercept-a5wm
title: '4-B: Prediction chip on /upcoming fight rows (visual slice closes)'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

User-visible: every fight row shows the model's pick.

- [ ] event-fight-card.tsx: for each fight row, fetch /api/predict/fight/:id when both fighters are state='current'
- [ ] Render a small chip after the weight-class badge: '58% Khamzat ✓' style
- [ ] If either fighter not loaded: 'Backfill required' chip (greyed out)
- [ ] Test on UFC 328 main event after backfilling Khamzat + Strickland
