---
# intercept-tco0
title: Fresh out-of-sample market data validation
status: todo
type: epic
priority: high
created_at: 2026-05-13T00:57:05Z
updated_at: 2026-05-13T00:57:05Z
---

Import fresh FightOdds-covered UFC events after the locked historical holdout and evaluate only frozen report-only candidates before any further tuning.\n\nAcceptance criteria:\n- [ ] Use a fresh worktree and dedicated epic branch from fork/main.\n- [ ] Import or identify blocker for UFC FightOdds events after 2024-03-09.\n- [ ] Match fresh market rows to canonical UFC fights using existing DB data only.\n- [ ] Run frozen candidates only; no new tuning on fresh data.\n- [ ] Publish research-only evidence and keep writes_model_versions=false.\n- [ ] Open and merge one PR to StreamlinedStartup/intercept:main.
