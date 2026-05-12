---
# intercept-zlwa
title: 'D2-MCU-B: Select coverage-completion event candidates'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:33:26Z
updated_at: 2026-05-12T03:43:02Z
parent: intercept-p6uo
blocked_by:
    - intercept-8jp3
---

Acceptance criteria:
- [x] Analyze D2-HOC unmatched event/fight reasons and adjacent FightOdds UFC events.
- [x] Pick a deterministic candidate set expected to add at least 4 scored market-covered events with margin.
- [x] Produce a report-only candidate artifact with event IDs, dates, expected canonical matches, and risk notes.
- [x] Do not import new odds rows in this task.

Notes:
- Start from the D2-HOC final report: 26/30 scored events, 220 review rows, 4-event shortfall.

## Summary of Changes

- Selected four already-imported rematch candidates where FightOdds event names differ from canonical UFCStats event names.
- Selected seven immediately prior UFC FightOdds events as supplemental import margin if rematching alone does not close the 4-event gap.
- Published report-only candidate artifacts with event IDs, dates, canonical matches, risk notes, and next import/match commands.

## Verification

- `jq empty data/experiments/market-coverage-unlock-candidates.json`
- `psql 'postgres://interceptor:interceptor@localhost:5434/interceptor' -c "select ... from historical_odds_events where canonical_event_id is null order by event_date;"`
- `psql 'postgres://interceptor:interceptor@localhost:5434/interceptor' -c "select ... from events ... order by date;"`
