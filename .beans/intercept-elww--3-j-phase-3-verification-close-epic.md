---
# intercept-elww
title: '3-J: Phase 3 verification + close epic'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T01:33:10Z
parent: intercept-at4c
blocked_by:
    - intercept-azd1
---

Verification per docs/ufc-fight-predictor-plan.md#phase-3.

- [x] python -m ml.train prints metrics; log_loss < 0.66 target
- [x] model_versions has the new row
- [x] ml.predict for (Khamzat, Strickland, 2026-05-09) returns {predicted_winner_id, win_prob in (0,1), contributing_features: [...]}
- [x] All unit tests pass (pytest)
- [x] biome + typecheck + vitest green
- [x] Mark E3 completed

## Summary of Changes

- Verified Phase 3 model training: `model_id=20260510T012856362940Z`, `training_set_size=80`, `log_loss=0.6213893292960028`, `accuracy=0.6875`.
- Confirmed latest `model_versions` row points at `data/models/20260510T012856362940Z.json`.
- Verified JSON-RPC `ml.predict` for Khamzat Chimaev (`767755fd74662dbf`) vs Sean Strickland (`0d8011111be000b2`) on `2026-05-09`: predicted Khamzat with `win_prob=0.6542974710464478` and returned `contributing_features`.
- Removed an unused web URL-state type so Biome has no warnings.
- Completed Phase 3 epic `intercept-at4c`.
