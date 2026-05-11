---
# intercept-5rw9
title: Historical odds source + odds-aware evaluation
status: todo
type: epic
priority: normal
created_at: 2026-05-11T13:30:39Z
updated_at: 2026-05-11T17:11:09Z
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
- [ ] FightOdds.io source posture and technical shape are documented before scraper/import work starts.
- [ ] Historical odds schema/import contract is designed with source metadata, timestamp semantics, sportsbook support, and unmatched review rows.
- [ ] One known event, UFC Fight Night 237 / Moreno vs Royval 2, is imported and matched first.
- [ ] A one-event odds-aware report joins walk-forward predictions to historical market odds.
- [ ] Multi-event backfill is added only after the one-event slice is proven.
- [ ] Final report prioritizes market-aware metrics: no-vig edge, ROI by flat stake, confidence buckets, edge buckets, market calibration, and CLV if available.
- [ ] Accuracy, log loss, Brier score, and ROC AUC appear only as secondary context.
- [ ] If any HTTP or UI surface is added, the epic includes an agent-browser smoke gate with screenshot evidence under data/smoke/.

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
