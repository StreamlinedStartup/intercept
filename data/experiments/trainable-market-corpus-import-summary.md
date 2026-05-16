# Trainable Market-Corpus Import Summary

- Generated: `2026-05-12T04:29:15Z`
- Report-only: `true`
- Writes `model_versions`: `false`

## Import

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 4592,4579,4580,4556,4501,4483,4486,4450,4469,4460,4438,4441,4382,4426 --delay-ms 1500 --continue-on-error
```

| Metric | Count |
|---|---:|
| Events scanned | 14 |
| Events imported | 14 |
| Events failed | 0 |
| Fights read | 209 |
| Moneyline rows read | 10,966 |
| Unmatched rows created | 209 |
| Cancelled fights | 38 |
| Skipped moneyline rows | 826 |

## Post-Import Database Counts

| Metric | Count |
|---|---:|
| FightOdds events | 51 |
| Matched FightOdds events | 37 |
| Target fights | 209 |
| Target moneyline rows | 10,966 |
| `model_versions` rows | 14 |

The target batch expanded the FightOdds date range to `2023-01-14` through `2024-03-09`. Matching remains the next step; the newly imported older events are intentionally unmatched until deterministic rematch tooling runs.
