# Prop Corpus Expansion Plan

Date: 2026-05-16
Bean: `intercept-oiry`
Status: report-only import plan

## Cohort

Use the existing matched FightOdds event corpus already present in Postgres:

- Source: `historical_odds_events`
- Filter: `source = 'fightodds'`, `match_status = 'matched'`, `canonical_event_id IS NOT NULL`
- Events: 81
- Existing prop coverage before this batch: 1 event, 12 distance markets, 294 prop rows

Event PKs, newest first:

```text
9010,8994,8959,8946,8861,8898,8832,8822,8830,8823,8814,8828,8813,8805,8768,8609,8620,6603,8597,8596,6668,6593,6553,6619,6552,6602,6414,6547,6511,6488,5356,5318,5362,5355,5358,5347,5306,5293,4779,5281,5251,4778,5098,4777,4655,5107,4776,4775,4774,4749,4802,4755,4727,4738,4751,4744,4671,4702,4634,4696,4668,4666,4654,4643,4627,4615,4594,4592,4579,4580,4556,4501,4483,4486,4450,4469,4460,4438,4441,4382,4426
```

## Import Command

Run the existing FightOdds importer with prop import enabled:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 9010,8994,8959,8946,8861,8898,8832,8822,8830,8823,8814,8828,8813,8805,8768,8609,8620,6603,8597,8596,6668,6593,6553,6619,6552,6602,6414,6547,6511,6488,5356,5318,5362,5355,5358,5347,5306,5293,4779,5281,5251,4778,5098,4777,4655,5107,4776,4775,4774,4749,4802,4755,4727,4738,4751,4744,4671,4702,4634,4696,4668,4666,4654,4643,4627,4615,4594,4592,4579,4580,4556,4501,4483,4486,4450,4469,4460,4438,4441,4382,4426 --include-props --delay-ms 1500 --continue-on-error
```

## Constraints

- Import only the `DISTANCE` market into `historical_prop_odds`; skip all other prop families with explicit reason counts.
- Preserve moneyline import semantics and existing `historical_moneyline_odds` behavior.
- Use `source_current` rows for primary harness scoring; keep `source_previous` as coverage only because FightOdds does not expose the previous-price timestamp in this query shape.
- Keep all downstream outputs report-only with `writes_model_versions = false`.
