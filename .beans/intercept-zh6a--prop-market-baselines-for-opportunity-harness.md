---
# intercept-zh6a
title: Prop market baselines for opportunity harness
status: completed
type: epic
priority: high
created_at: 2026-05-16T00:51:26Z
updated_at: 2026-05-16T01:03:57Z
parent: intercept-8mw9
---

Connect imported FightOdds DISTANCE prop odds to the report-only market opportunity harness so decision and finish likelihood targets can evaluate against real market baselines. Scope: config/plan, prop baseline loader, target ROI/gate integration, report artifacts, and verification. Do not activate betting recommendations or model promotion.

## Summary of Changes

- Mapped `historical_prop_odds` `DISTANCE` rows into no-vig decision and finish market baselines.
- Wired decision/finish target ROI and gate comparison to prop-backed market baselines while preserving unavailable status when coverage is missing.
- Refreshed `market-opportunity-matrix-v1`; `finish_edge_log_c1_conf62` ranks first but remains research-only and fails the configured market gate.
