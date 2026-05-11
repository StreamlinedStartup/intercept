---
# intercept-ovyg
title: 'D2-HO-C: Import one FightOdds event moneyline slice'
status: todo
type: task
created_at: 2026-05-11T17:11:46Z
updated_at: 2026-05-11T17:11:46Z
parent: intercept-5rw9
blocked_by:
    - intercept-t19g
---

Acceptance criteria:
- [ ] Implement only the UFC Fight Night 237 / Moreno vs Royval 2 import slice from the approved source shape.
- [ ] Import moneyline odds for the candidate event without broad pagination or many-event scraping.
- [ ] Persist source event/fight IDs, source URLs, raw fighter names, sportsbook when available, American odds, decimal odds, and raw metadata.
- [ ] Make the import idempotent for repeat local runs.
- [ ] Preserve unmatched or ambiguous rows for review rather than dropping them.
- [ ] Keep production prediction serving unchanged.

Verification:
- Import command or script reports rows read, rows inserted/updated, rows matched, and rows unmatched.
- Database query confirms only the one target event was imported.
- Tests or focused command output verify American-to-decimal conversion if conversion is implemented here.
