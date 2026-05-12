---
# intercept-gvur
title: 'D2-RV-Sm: agent-browser smoke gate'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:32Z
updated_at: 2026-05-12T01:29:11Z
parent: intercept-dmyw
blocked_by:
    - intercept-x08v
---

Final HTTP/UI smoke gate for the model reliability epic.

Acceptance criteria:
- [x] Start the dev stack for the relevant UI surfaces.
- [x] Use agent-browser on /upcoming and /predictions.
- [x] Capture committed screenshot evidence under data/smoke/.
- [x] Verify the UI does not imply a validated betting edge unless the gate has passed.

## Summary of Changes
- Captured `/upcoming` smoke evidence at `data/smoke/d2-rv-upcoming-market-comparison.png`.
- Captured `/predictions` smoke evidence at `data/smoke/d2-rv-predictions-research-only.png`.
- Verified the visible UI uses market comparison, research-only, and research filter wording rather than validated betting-edge language.

## Verification
- `agent-browser open http://localhost:3000/upcoming`
- `agent-browser screenshot data/smoke/d2-rv-upcoming-market-comparison.png`
- `agent-browser open http://localhost:3000/predictions`
- `agent-browser screenshot data/smoke/d2-rv-predictions-research-only.png`
- `agent-browser eval 'document.body.innerText'`
