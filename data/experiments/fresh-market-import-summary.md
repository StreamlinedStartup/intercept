# Fresh Market Import Summary

- Generated: 2026-05-13
- Source: FightOdds sitemap plus existing explicit-PK importer
- Fresh criterion: imported UFC FightOdds events after `2024-03-09`
- Import mode: explicit event PKs, avoiding the rate-limited `allEvents` pagination endpoint
- Report only: `true`
- Writes `model_versions`: `false`

## Import

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db import:fightodds:event -- \
  --event-pks 9010,8994,8959,8946,8861,8898,8832,8822,8830,8823,8814,8828,8813,8805,8768,8609,8620,6603,8597,8596,6668,6593,6553,6619,6552,6602,6414,6547,6511,6488 \
  --delay-ms 1500 \
  --continue-on-error
```

Result:

- Events imported: 30
- Failed events: 0
- Source fights read: 438
- Moneyline rows read: 35,046
- Cancelled fights: 52

## Match

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db match:fightodds:all
```

Fresh post-`2024-03-09` result:

- Fresh events: 30
- Source fights: 438
- Matched fights: 310
- Moneyline rows: 35,046
- Linked moneyline rows: 26,260

Combined FightOdds corpus after matching:

- Source events: 81
- Matched source events: 81
- Source fights: 1,219
- Matched fights: 809
- Ambiguous fights: 1
- Linked moneyline rows: 54,298

## Notes

The initial date-range importer hit `HTTP 429` on FightOdds `EventsRecentQuery`.
This run used the existing explicit event-PK path from sitemap-discovered URLs
instead of retrying the paginated endpoint.
