---
# intercept-gopa
title: 'D2-HO-D: Match historical odds rows to canonical fights'
status: todo
type: task
created_at: 2026-05-11T17:11:53Z
updated_at: 2026-05-11T17:11:53Z
parent: intercept-5rw9
blocked_by:
    - intercept-ovyg
---

Acceptance criteria:
- [ ] Match FightOdds events to canonical DB events using date, promotion, normalized event name, and source metadata.
- [ ] Match fights using event date, UFC promotion, normalized fighter names, aliases when available, sorted fighter pairs, and weight class when available.
- [ ] Correctly handle swapped fighter order.
- [ ] Explicitly handle missing accents, punctuation differences, nicknames, renamed fighters, cancelled bouts, and rebooked bouts.
- [ ] Preserve ambiguous and unmatched rows with a review reason and candidate canonical matches.
- [ ] Produce match-rate and unmatched-rate summary output for the one-event slice.

Verification:
- Unit tests cover name normalization, swapped fighter order, accent/punctuation normalization, and ambiguous matches.
- One-event import shows matched canonical fight/fighter IDs where possible and review rows where not possible.
