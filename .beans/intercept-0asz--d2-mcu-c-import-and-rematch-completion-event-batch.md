---
# intercept-0asz
title: 'D2-MCU-C: Import and rematch completion event batch'
status: todo
type: task
priority: high
created_at: 2026-05-12T03:33:31Z
updated_at: 2026-05-12T03:33:31Z
parent: intercept-p6uo
blocked_by:
    - intercept-zlwa
---

Acceptance criteria:
- [ ] Import the approved completion candidate FightOdds events into historical_odds_events, historical_odds_fights, historical_moneyline_odds, and unmatched_historical_odds.
- [ ] Run deterministic event/fight rematching after import.
- [ ] Preserve cancelled-bout handling and unresolved reason reporting.
- [ ] Report imported events, imported fights, matched fights, linked moneyline rows, and failed imports.

Constraints:
- Keep importer/report tooling report-only for model validation purposes.
- Do not write active model_versions.
