---
# intercept-1fhe
title: '2-F: Phase 2 verification + close epic'
status: todo
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T19:25:17Z
parent: intercept-8gxf
blocked_by:
    - intercept-zfc6
---

Verification per docs/ufc-fight-predictor-plan.md#phase-2.

- [ ] curl localhost:3001/api/odds-mma/upcoming returns JSON with current MMA odds; X-Cache MISS then HIT
- [ ] curl localhost:3001/api/odds-mma/snapshot writes rows; SELECT count from odds_snapshots > 0
- [ ] Matcher logs matched/unmatched summary, and unmatched rows are persisted when canonical fights are absent
- [ ] x-requests-remaining shows budget consumption
- [ ] biome + typecheck + vitest green
- [ ] Hand off to 2-Sm smoke gate (epic stays open until that passes)
