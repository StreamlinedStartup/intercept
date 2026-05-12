---
# intercept-p6uo
title: 'D2-MCU: Market coverage unlock to 30 scored events'
status: todo
type: epic
priority: high
created_at: 2026-05-12T03:33:06Z
updated_at: 2026-05-12T03:33:06Z
parent: intercept-8mw9
---

Restore a green baseline, finish market-covered event coverage, and rerun the validation gate so model-improvement work has enough scored events to proceed responsibly.

Acceptance criteria:
- [ ] CI/package baseline is green or the remaining blocker is isolated and documented before corpus work continues.
- [ ] Coverage-completion candidates are selected from unresolved D2-HOC gaps and/or adjacent FightOdds UFC events.
- [ ] Historical odds imports and rematching reach at least 30 scored market-covered UFC events or publish a reportable blocker.
- [ ] Leakage audit, baselines, coverage, and market gate are rerun after the coverage-completion work.
- [ ] Final unlock report states whether model-improvement experiments are unblocked.

Constraints:
- Keep all reports research-only unless the market gate truly passes.
- Do not tune XGBoost in this epic.
- Do not activate validated status unless coverage and ROI thresholds truly pass.
- Do not write active model_versions.
- Preserve unrelated dirty files and stashes.
