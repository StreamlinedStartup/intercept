---
# intercept-41ei
title: 'D2-HO-G: Final odds-aware verification and report'
status: todo
type: task
created_at: 2026-05-11T17:12:14Z
updated_at: 2026-05-11T17:12:14Z
parent: intercept-5rw9
blocked_by:
    - intercept-xbke
---

Acceptance criteria:
- [ ] Produce final odds-aware evaluation artifacts, preferably data/experiments/odds-aware-evaluation.json and data/experiments/odds-aware-evaluation.md.
- [ ] Report ROI by flat stake, edge bucket, confidence bucket, and market-favorite baseline.
- [ ] Report no-vig edge, calibration versus market, and closing-line value if the source provides open/close or timestamped lines.
- [ ] Include secondary model-quality context: accuracy, log loss, Brier score, and ROC AUC.
- [ ] Document source coverage, unmatched rate, timestamp limitations, and whether FightOdds.io remains the recommended historical source.
- [ ] Verify production predictions were not changed by this research epic.
- [ ] Decide whether an agent-browser smoke bean is required based on whether any HTTP or UI surface was added.

Verification:
- Run focused unit/integration tests for importer, matcher, odds math, and report generation.
- Run the final report command and commit generated evidence.
- If HTTP/UI was added, create and complete a final D2-HO-Sm agent-browser smoke gate with screenshot evidence under data/smoke/ before closing the epic.
