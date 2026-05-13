---
# intercept-tco0
title: Fresh out-of-sample market data validation
status: completed
type: epic
priority: high
created_at: 2026-05-13T00:57:05Z
updated_at: 2026-05-13T01:15:23Z
---

Import fresh FightOdds-covered UFC events after the locked historical holdout and evaluate only frozen report-only candidates before any further tuning.\n\nAcceptance criteria:\n- [x] Use a fresh worktree and dedicated epic branch from fork/main.\n- [x] Import or identify blocker for UFC FightOdds events after 2024-03-09.\n- [x] Match fresh market rows to canonical UFC fights using existing DB data only.\n- [x] Run frozen candidates only; no new tuning on fresh data.\n- [x] Publish research-only evidence and keep writes_model_versions=false.\n- [x] Open and merge one PR to StreamlinedStartup/intercept:main.



## Summary of Changes

- Imported and matched 30 fresh post-holdout FightOdds UFC events.
- Evaluated three frozen candidates on the fresh slice; none cleared the market gate.
- Ran a 7,777-variant fresh selected-fight search; zero variants cleared the market gate.
- Kept all artifacts report-only / research_only with writes_model_versions=false.

## Recommendation

Current model families and selected-fight threshold tuning still do not validate against the market on fresh data. The next useful work is new signal quality or line/entity quality, not more blend/confidence tuning over the same features.
