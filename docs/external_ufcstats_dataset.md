# External UFC Stats Dataset Integration

This doc scopes how we should incorporate [`Greco1899/scrape_ufc_stats`](https://github.com/Greco1899/scrape_ufc_stats) into the UFC Fight Predictor workflow.

## Why Use It

Our current predictor can scrape `ufcstats.com` through our own `domains/ufcstats` plugin, but that is the wrong default path for model iteration and backtesting.

The external project already publishes the same core UFC Stats data as committed CSV files and refreshes them daily. For our use case, that gives us:

- a larger historical corpus without hammering `ufcstats.com`;
- a repeatable local snapshot for training experiments;
- a clean input for walk-forward backtests;
- faster model-tuning loops because CSV import is cheaper than live scraping.

We should keep our own scraper for product-facing freshness and spot checks, but use the external CSV snapshot as the default model research corpus.

## Source Summary

The upstream repo describes itself as scraping UFC events, fight stats, and fighter details from `ufcstats.com` into CSV format. It publishes these CSVs:

| Upstream file | Likely use in our DB |
|---|---|
| `ufc_event_details.csv` | `events` |
| `ufc_fight_details.csv` | fight metadata supplement |
| `ufc_fight_results.csv` | `fights` and fight-level result fields |
| `ufc_fight_stats.csv` | `fight_round_stats` and rolled-up `fight_results` stats |
| `ufc_fighter_details.csv` | fighter profile and current summary stats |
| `ufc_fighter_tott.csv` | fighter tale-of-the-tape fields |

The README says the project runs a daily Cloud Run job through Cloud Scheduler to check for new fights/fighters, refresh the CSV files, and push the refreshed data back to the repository. It also says a manual full refresh happened on November 22, 2025.

## License Boundary

The upstream repository is GPL-3.0 licensed.

For this project, the safest integration shape is:

- do not copy upstream scraper code;
- do not vendor upstream notebooks or Python library files;
- download CSV data as an external input at operator/runtime time;
- record source URL, commit SHA, ETag, and retrieval timestamp for reproducibility;
- document attribution and the upstream license in generated snapshot metadata;
- keep downloaded CSV files out of normal git commits unless we make an explicit licensing decision later.

This is not legal advice. It is an engineering boundary that avoids mixing GPL scraper code into our codebase while still letting us use public factual fight data for local model research.

## Target Architecture

Add an external dataset ingestion path alongside the current live scraper.

```text
GitHub CSV snapshot
  -> local ignored data/external/ufcstats/<snapshot-id>/*.csv
  -> importer validation + normalization
  -> canonical Postgres tables
  -> training and walk-forward backtesting
```

The canonical DB remains the source of truth for the model. The external CSVs are an input format, not a new parallel schema.

## Snapshot Download

Download the current upstream CSV snapshot with:

```bash
pnpm data:ufcstats:snapshot
```

The command writes only the six published CSVs and `metadata.json` under:

```text
data/external/ufcstats/<snapshot-id>/
```

`data/external/` is ignored by git through the existing `/data/*` rule. Do not stage downloaded CSV snapshots unless we make an explicit licensing and reproducibility decision later.

Useful options:

```bash
pnpm data:ufcstats:snapshot -- --ref main
pnpm data:ufcstats:snapshot -- --snapshot-id manual-2026-05-11
pnpm data:ufcstats:snapshot -- --out-dir /tmp/ufcstats-snapshots
```

Snapshot metadata records the source repository, requested ref, resolved commit SHA, retrieval timestamp, upstream license note, and each file's raw URL, ETag, size, content type, and SHA-256 hash.

## Import Principles

The importer should be strict and boring:

- fail loudly if a required CSV is missing;
- fail loudly if a required column is missing or renamed;
- derive stable IDs from existing UFC Stats URLs when possible;
- normalize event names and fighter names only at matching boundaries;
- preserve raw source values in logs or import metadata when a row cannot be mapped;
- upsert idempotently so re-importing the same snapshot is safe;
- never silently drop a fight row.

Import a downloaded snapshot into the canonical predictor tables with:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:ufcstats data/external/ufcstats/<snapshot-id>
```

The importer validates the snapshot hashes from `metadata.json`, derives UFC Stats IDs from source URLs, upserts canonical rows, and refreshes `fighter_backfill_state` so imported fighters are marked `current` with their imported history counts.

Rows that cannot be identified from the CSV snapshot alone, such as duplicate fighter names without fighter URLs in fight rows, are skipped with explicit counts in the command output instead of being guessed.

## DB Mapping

### Events

Use `ufc_event_details.csv` to populate:

- `events.id`
- `events.name`
- `events.date`
- `events.location`
- `events.completed`
- `events.promotion`

All imported rows from this source should default to `promotion='ufc'` unless the source clearly marks otherwise.

### Fights And Results

Use `ufc_fight_results.csv` for:

- event name;
- bout pairing;
- winner/loser/draw outcome;
- weight class;
- method and method details;
- round and ending time;
- scheduled format;
- fight detail URL.

The fight detail URL contains the strongest stable fight ID. We should derive `fights.id` from that URL when present.

### Round Stats

Use `ufc_fight_stats.csv` for one row per fighter per round:

- knockdowns;
- significant strikes landed/attempted;
- total strikes landed/attempted;
- takedowns landed/attempted;
- submission attempts;
- reversals;
- control time;
- head/body/leg splits;
- distance/clinch/ground splits.

The importer should also roll these rows up into fight-level `fight_results` totals because the current feature builder reads career stats from `fight_results`.

### Fighters

Use `ufc_fighter_details.csv` and `ufc_fighter_tott.csv` for:

- fighter name;
- DOB;
- height;
- reach;
- stance;
- current career summary fields where available.

If the upstream CSV lacks a stable fighter URL in a row, the importer should match by normalized fighter name and report ambiguous matches instead of guessing.

## Backtesting Plan

The external dataset unlocks the backtest we actually need: walk-forward backtesting.

The runner should:

1. Import one external CSV snapshot into a clean or namespaced local DB.
2. Sort completed UFC events by date.
3. Pick a start date where enough prior fights exist to train.
4. Train on fights before the target event.
5. Predict every fight on the target event using only pre-event data.
6. Score those predictions against actual results.
7. Move to the next event and repeat.

Report outputs should include:

- accuracy;
- log loss;
- Brier score;
- ROC AUC where valid;
- calibration by probability bucket;
- performance by confidence bucket;
- performance by feature regime, such as debut fights, long layoffs, and weight-class changes;
- ROI by edge bucket when odds exist.

The rule is the same as our model scope doc: every simulated prediction must use only data that would have existed before that event.

## Relationship To Live Scraping

This source should not replace our live UFC Stats domain entirely.

Use the external CSV dataset for:

- initial corpus building;
- model feature experiments;
- walk-forward backtesting;
- repeatable training fixtures.

Use our live `domains/ufcstats` plugin for:

- upcoming cards;
- UI-driven freshness checks;
- post-event spot refresh;
- validating that the external CSV schema has not drifted from the live site.

## Implementation Beans

This integration is tracked under `intercept-r03n`.

Recommended order:

1. `intercept-bsn7`: scope this integration and document the data/license boundary.
2. `intercept-n89z`: add a download command for the external CSV snapshot.
3. `intercept-0vfw`: map the CSVs into canonical predictor DB tables.
4. `intercept-pqsx`: add a walk-forward backtest runner.
5. `intercept-u1vf`: expose backtest reports for model tuning comparisons.
