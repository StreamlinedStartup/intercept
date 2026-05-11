---
# intercept-zivm
title: 'D2-HO-A: Discover FightOdds and compare historical odds sources'
status: todo
type: task
priority: normal
created_at: 2026-05-11T13:31:22Z
updated_at: 2026-05-11T17:11:21Z
parent: intercept-5rw9
blocked_by:
    - intercept-qizd
---

Acceptance criteria:
- [ ] Inspect FightOdds.io with Intercept/browser traffic discovery and agent-browser.
- [ ] Check robots.txt, terms, and rate-limit posture before scraping.
- [ ] Determine whether the event and odds pages are server-rendered, embedded JSON, API-backed, or JS-rendered.
- [ ] Identify event index/list routes, event detail routes, odds routes, pagination, stable source IDs, and query parameters.
- [ ] Capture the technical shape for UFC Fight Night 237 / Moreno vs Royval 2 event and odds pages.
- [ ] Compare ESPN, Covers, and FightMatrix fallback viability for the same event.
- [ ] Recommend whether FightOdds.io should remain the primary source before schema/import work starts.

Candidate URLs:
- https://fightodds.io/mma-events/5362/ufc-fight-night-237-moreno-vs-royval-2
- https://fightodds.io/mma-events/5362/ufc-fight-night-237-moreno-vs-royval-2/odds
- https://www.espn.com/mma/fightcenter/_/id/600041054
- https://www.covers.com/sport/mma/ufc/card-ufc-fight-night-odds-6472
- https://www.fightmatrix.com/2024/02/19/select-fight-matrix-program-ufc-fight-night-moreno-vs-royval-2-02-23-2024/

Verification:
- Save discovery notes in the bean summary.
- Include enough request/selector evidence to justify the source recommendation.
- Do not implement an importer in this task.
