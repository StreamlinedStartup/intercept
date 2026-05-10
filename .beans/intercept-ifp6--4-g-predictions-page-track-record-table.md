---
# intercept-ifp6
title: '4-G: /predictions page — track record table'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-lmh6
---

First version of the user-facing track-record page.

- [ ] apps/web/src/app/(dashboard)/predictions/page.tsx + predictions-content.tsx
- [ ] Header: model version + training date + log_loss + brier + accuracy + n_predictions
- [ ] Table: last 50 predictions; columns Date / Fighter / Pick / WinProb / Vegas / Result / ✓✗
- [ ] Sidebar nav entry 'Predictions' added (CalendarRange or similar icon)
- [ ] Empty state when no predictions yet
