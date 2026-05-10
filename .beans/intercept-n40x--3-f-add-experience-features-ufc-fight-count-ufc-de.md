---
# intercept-n40x
title: '3-F: Add experience features (UFC fight count + ufc_debut)'
status: todo
type: task
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-09T19:02:04Z
parent: intercept-at4c
blocked_by:
    - intercept-84gp
---

ufc_fight_count_a, _b, _diff + ufc_debut bool. Filter on events.promotion='ufc'.

- [ ] features.py adds experience features
- [ ] Test: fighter with 0 prior UFC fights → ufc_debut=true, ufc_fight_count_a=0
- [ ] Test: a non-UFC fight (e.g. Bellator) doesn't increment ufc_fight_count
- [ ] Re-train and check log_loss change
