---
# intercept-aeef
title: 'D2-RV-D: Expand historical odds match coverage'
status: todo
type: task
priority: high
created_at: 2026-05-12T00:21:19Z
updated_at: 2026-05-12T00:21:19Z
parent: intercept-dmyw
blocked_by:
    - intercept-tjvc
---

Improve historical odds match coverage before using market comparisons for any validation claim.

Acceptance criteria:
- [ ] Expand canonical matching coverage across more UFC events.
- [ ] Keep unmatched rows reviewable instead of silently dropping them.
- [ ] Report coverage by source event, canonical event, fights, and fighter rows.
- [ ] Do not write active model_versions.
