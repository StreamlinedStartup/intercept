---
# intercept-t19g
title: 'D2-HO-B: Design historical odds schema and import contract'
status: todo
type: task
created_at: 2026-05-11T17:11:38Z
updated_at: 2026-05-11T17:11:38Z
parent: intercept-5rw9
blocked_by:
    - intercept-zivm
---

Acceptance criteria:
- [ ] Decide whether to extend odds_snapshots or create dedicated historical odds tables.
- [ ] Define source, source_event_id, source_fight_id, source_url, sportsbook, line kind, American odds, decimal odds, implied probability, scrape timestamp, and market timestamp semantics.
- [ ] Define raw metadata storage for event, fight, and odds rows.
- [ ] Define unmatched historical odds review storage with raw names, candidate matches, reason, and reviewed flag.
- [ ] Document how historical odds differ from live odds snapshots, especially when only closing/current lines are available.
- [ ] Keep production predictions unchanged.

Data model sketch:
- historical_odds_events: source event identity and canonical event link.
- historical_odds_fights: source fight identity, raw fighter pair, canonical fight link, weight class, status.
- historical_moneyline_odds: source fight, sportsbook, raw fighter, canonical fighter link, line kind, American/decimal odds, observed timestamp when available.
- unmatched_historical_odds: raw event/fight/fighter fields, source IDs, reason, candidate matches, reviewed flag.

Verification:
- Schema/import design is captured in this bean summary or a focused docs/data-model note.
- No importer is implemented in this task.
