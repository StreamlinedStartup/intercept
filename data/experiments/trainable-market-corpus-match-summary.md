# Trainable Market-Corpus Match Summary

- Generated: `2026-05-12T04:33:05Z`
- Report-only: `true`
- Writes `model_versions`: `false`

## Match Run

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all
```

| Metric | Count |
|---|---:|
| Events matched | 51/51 |
| Fights matched | 499/781 |
| Ambiguous fights | 0 |
| Unmatched fights | 282 |
| Cancelled unmatched fights | 162 |
| Moneyline rows linked | 28,038 |

## Target Batch

| Metric | Count |
|---|---:|
| Events matched | 14/14 |
| Fights matched | 140/209 |
| Cancelled unmatched fights | 38 |
| Moneyline rows linked | 7,843/10,966 |

## Regression Check

The existing 37-event corpus remains matched at 37/37 events.

## Matching Changes

- Added participant-overlap event fallback for same-date UFC events whose FightOdds headline changed before fight night.
- Added `Dontale Mayes` / `Don'Tale Mayes` name alias for participant matching.

## Review Reasons

| Reason | Rows |
|---|---:|
| source fight is cancelled and no canonical fight pair exists on the completed event | 162 |
| no canonical fight matched normalized fighter pair | 120 |

`model_versions` remained unchanged at 14 rows.
