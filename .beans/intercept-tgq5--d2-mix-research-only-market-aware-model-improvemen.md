---
# intercept-tgq5
title: 'D2-MIX: Research-only market-aware model improvement experiments'
status: todo
type: epic
priority: high
created_at: 2026-05-12T03:33:57Z
updated_at: 2026-05-12T03:33:57Z
parent: intercept-8mw9
blocked_by:
    - intercept-136k
---

Run report-only model-improvement experiments only after the D2-MCU unlock decision says coverage is sufficient. The goal is to improve model quality against the market favorite without activating claims prematurely.

Acceptance criteria:
- [ ] Experiment inputs are frozen from the D2-MCU coverage-passing, research-only market gate bundle.
- [ ] Calibration, blend, and feature/model variants are evaluated with walk-forward discipline.
- [ ] Every result compares against the no-vig market favorite baseline.
- [ ] Outputs are JSON/Markdown research artifacts only.
- [ ] No active model_versions writes or validated activation happen in this epic.

Constraints:
- Do not start until D2-MCU-F says research-only model-improvement experiments are unblocked.
- Keep UI/API/docs research-only unless a separate activation gate passes.
