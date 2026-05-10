---
# intercept-n40x
title: '3-F: Add experience features (UFC fight count + ufc_debut)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T01:11:29Z
parent: intercept-at4c
blocked_by:
    - intercept-84gp
---

ufc_fight_count_a, _b, _diff + ufc_debut bool. Filter on events.promotion='ufc'.

- [x] features.py adds experience features
- [x] Test: fighter with 0 prior UFC fights → ufc_debut=true, ufc_fight_count_a=0
- [x] Test: a non-UFC fight (e.g. Bellator) doesn't increment ufc_fight_count
- [x] Re-train and check log_loss change

## Summary of Changes

- Added `ufc_fight_count_a`, `ufc_fight_count_b`, `ufc_fight_count_diff`, and `ufc_debut` to `FEATURE_NAMES`.
- Counted prior UFC fights with `events.promotion='ufc'` and `event.date < target_fight.date`; `ufc_debut` is true when either fighter has zero prior UFC fights.
- Added DB-backed pytest coverage for debutants and non-UFC prior fights.
- Retrain result: `model_id=20260510T011033997514Z`, `log_loss=0.5968872791151922`, improved from `0.6214818254404825`.
