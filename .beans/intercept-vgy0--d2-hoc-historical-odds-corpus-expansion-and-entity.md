---
# intercept-vgy0
title: 'D2-HOC: Historical odds corpus expansion and entity-resolution gate'
status: todo
type: epic
priority: high
created_at: 2026-05-12T02:27:20Z
updated_at: 2026-05-12T02:27:20Z
parent: intercept-8mw9
---

Expand the historical FightOdds corpus to the validation target and harden deterministic event/fight entity resolution before any model-improvement work.

Acceptance criteria:
- [ ] 30-event UFC target cohort is defined and documented.
- [ ] Baseline coverage is report-only and writes no active model_versions.
- [ ] Event and fight entity-resolution heuristics are improved and regression-checked on the current 3-event corpus.
- [ ] Target FightOdds event batch is imported into historical odds tables.
- [ ] Unmatched historical odds rows are reviewed/rematched with unresolved reasons reportable.
- [ ] Scaled coverage and market-gate reports state whether the >=200 fight / >=30 event gate passes.
- [ ] Final JSON and Markdown corpus expansion report are published.

Constraints:
- Keep UI/API/docs research-only unless validation truly passes.
- Do not tune XGBoost on the current 30-fight sample.
- Do not activate validated status.
- Do not write active model_versions.
- Do not build UI unless CLI review becomes a blocker.
