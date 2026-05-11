---
# intercept-5rw9
title: Historical odds source + odds-aware evaluation
status: completed
type: epic
priority: normal
created_at: 2026-05-11T13:30:39Z
updated_at: 2026-05-11T19:04:00Z
parent: intercept-8mw9
blocked_by:
    - intercept-qizd
---

Epic 2 for Decision Engine v2. Discover a public historical MMA odds source, prove a one-event moneyline import slice, match historical odds to canonical fights, and produce an odds-aware model evaluation report.

Scope:
- Treat FightOdds.io as the primary candidate source until discovery proves otherwise.
- Use Intercept/browser traffic discovery before assuming an API or DOM shape.
- Compare ESPN, Covers, and FightMatrix as fallback sources if FightOdds.io is blocked, hostile, incomplete, or technically fragile.
- Preserve production prediction behavior during the research epic.
- Do not copy GPL or third-party scraper code into this repo.
- Store unmatched historical odds rows for review instead of silently dropping them.

Acceptance criteria:
- [x] FightOdds.io source posture and technical shape are documented before scraper/import work starts.
- [x] Historical odds schema/import contract is designed with source metadata, timestamp semantics, sportsbook support, and unmatched review rows.
- [x] One known event, UFC Fight Night 237 / Moreno vs Royval 2, is imported and matched first.
- [x] A one-event odds-aware report joins walk-forward predictions to historical market odds.
- [x] Multi-event backfill is added only after the one-event slice is proven.
- [x] Final report prioritizes market-aware metrics: no-vig edge, ROI by flat stake, confidence buckets, edge buckets, market calibration, and CLV if available.
- [x] Accuracy, log loss, Brier score, and ROC AUC appear only as secondary context.
- [x] If any HTTP or UI surface is added, the epic includes an agent-browser smoke gate with screenshot evidence under data/smoke/.

Primary candidate:
- FightOdds.io remains the primary historical odds candidate after planning, but the first task decides whether it is actually usable.

Fallback candidates:
- ESPN fightcenter historical event pages.
- Covers historical MMA card odds.
- FightMatrix program pages with betting odds.

Operational rules:
- One epic branch: epic/intercept-5rw9-historical-odds-evaluation.
- Push and PR only to fork=https://github.com/StreamlinedStartup/intercept.git.
- Never push or submit PRs to origin=https://github.com/adam-s/intercept.git.
- Stage explicit file paths only.
- Commit each completed child bean separately.

## Summary of Changes

- Completed FightOdds.io discovery, schema/import contract, one-event import/match, one-event odds-aware report, bounded multi-event backfill, and final odds-aware evaluation.
- Added final artifacts at `data/experiments/odds-aware-evaluation.json` and `data/experiments/odds-aware-evaluation.md`.
- Final scored sample remains 12 fights from one matched event. Model-edge selections went 0-6 for -100.0% ROI; market favorites went 10-12 for +31.4% ROI.
- Source coverage now includes 3 imported FightOdds UFC events, 46 source fights, and 2173 moneyline rows; 2 events remain unmatched and reviewable.
- FightOdds remains the recommended historical source. Canonical event/fight matching coverage is the next blocker before drawing broader ROI conclusions.
- No agent-browser smoke gate was required because this epic added DB/Python research commands and generated artifacts, with no HTTP route or UI surface.

Verification:
- `services/python/.venv/bin/python -m pytest services/python/test_odds_aware_report.py -q`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/db test`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:odds-aware:evaluation`
- `beans check`
