# Historical Odds Coverage

- Generated: `2026-05-12T02:38:42.785Z`
- Source events: 3/3 matched
- Fights matched: 37/46 (80.4%)
- Moneyline rows linked: 1915/2173 (88.1%)
- Review rows: 55
- Writes `model_versions`: `false`

## Target Cohort

- Cohort: `d2-hoc-30-event`
- Window: 2023-01-01 <= event date < 2024-03-10
- Target UFC events: 3/30 imported (10.0%)
- Selection rule: Use FightOdds EventsRecentQuery with dateGte=2023-01-01, dateLt=2024-03-10, orderBy=-date, filter promotion slug/shortName to UFC, and import the first 30 UFC events.
- Import command: `pnpm --filter @interceptor/db import:fightodds:range -- --from 2023-01-01 --to 2024-03-10 --limit 30`
- Match command: `pnpm --filter @interceptor/db match:fightodds:all`
- Report command: `pnpm --filter @interceptor/db report:fightodds:coverage -- --target-cohort d2-hoc-30-event`
- Rationale: The window ends at UFC 299, which is the newest event in the current 3-event corpus, and reaches backward far enough for the importer to select 30 recent UFC market events without using future market data.

## Events

| Source event | Canonical event | Date | Status | Fights | Moneylines | Review rows |
|---|---|---:|---|---:|---:|---:|
| 5362 UFC Fight Night 237: Moreno vs. Royval 2 | 902ab9197b83d0db | 2024-02-24 | matched | 12/14 | 600/652 | 16 |
| 5318 UFC Fight Night 238: Rozenstruik vs. Gaziev | e4a9dbade7c7e1a7 | 2024-03-02 | matched | 11/16 | 508/688 | 21 |
| 5356 UFC 299: O'Malley vs. Vera 2 | a9df5ae20a97b090 | 2024-03-09 | matched | 14/16 | 807/833 | 18 |

Unmatched and ambiguous fights remain reviewable in `unmatched_historical_odds`; they are not silently dropped.
