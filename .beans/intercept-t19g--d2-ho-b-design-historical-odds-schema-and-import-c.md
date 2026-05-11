---
# intercept-t19g
title: 'D2-HO-B: Design historical odds schema and import contract'
status: completed
type: task
priority: normal
created_at: 2026-05-11T17:11:38Z
updated_at: 2026-05-11T17:49:27Z
parent: intercept-5rw9
blocked_by:
    - intercept-zivm
---

Acceptance criteria:
- [x] Decide whether to extend odds_snapshots or create dedicated historical odds tables.
- [x] Define source, source_event_id, source_fight_id, source_url, sportsbook, line kind, American odds, decimal odds, implied probability, scrape timestamp, and market timestamp semantics.
- [x] Define raw metadata storage for event, fight, and odds rows.
- [x] Define unmatched historical odds review storage with raw names, candidate matches, reason, and reviewed flag.
- [x] Document how historical odds differ from live odds snapshots, especially when only closing/current lines are available.
- [x] Keep production predictions unchanged.

Data model sketch:
- historical_odds_events: source event identity and canonical event link.
- historical_odds_fights: source fight identity, raw fighter pair, canonical fight link, weight class, status.
- historical_moneyline_odds: source fight, sportsbook, raw fighter, canonical fighter link, line kind, American/decimal odds, observed timestamp when available.
- unmatched_historical_odds: raw event/fight/fighter fields, source IDs, reason, candidate matches, reviewed flag.

Verification:
- Schema/import design is captured in this bean summary or a focused docs/data-model note.
- No importer is implemented in this task.

## Summary of Changes

Historical odds should use dedicated tables instead of extending `odds_snapshots`. The existing `odds_snapshots` table is a Timescale/current-snapshot serving table used by production prediction APIs, keyed around canonical fights/fighters and observed live bookmaker snapshots. FightOdds historical rows have different semantics: source event/fight identity is primary, canonical matching can be incomplete, and the discovered event query exposes sportsbook moneylines as source-current and previous values without a source-provided market timestamp.

Proposed import contract:
- `historical_odds_import_runs`: one row per importer run with `source`, `started_at`, `finished_at`, `status`, `source_url`, event/fight/odds counts, matched/unmatched counts, and raw run metadata.
- `historical_odds_events`: `source`, `source_event_id`, `source_event_global_id`, `source_slug`, `source_url`, `raw_name`, `event_date`, `venue`, `city`, `promotion`, nullable `canonical_event_id`, `match_status`, `match_reason`, `raw_metadata`, `scraped_at`, `created_at`, and `updated_at`. Unique key: `(source, source_event_id)`.
- `historical_odds_fights`: `historical_event_id`, `source_fight_id`, `source_fight_slug`, `source_url`, raw fighter names, source fighter IDs/slugs, `is_cancelled`, `prop_count`, discovered best odds, nullable canonical fight/fighter links, `match_status`, `match_reason`, candidate matches, raw metadata, and timestamps. Unique key: `(historical_event_id, source_fight_id)`.
- `historical_moneyline_odds`: `historical_fight_id`, `source_offer_id`, sportsbook ID/slug/name, source outcome ID, raw fighter name, source fighter ID, nullable canonical fighter link, side (`fighter_a` or `fighter_b`), `line_kind`, American odds, decimal odds, implied probability, nullable `market_timestamp`, `market_timestamp_semantics`, `scraped_at`, and raw metadata. Unique key should be deterministic per import run and source outcome, for example `(import_run_id, source_offer_id, source_outcome_id, line_kind)`.
- `unmatched_historical_odds`: `source`, source event/fight IDs, source URL, raw event date/name, raw fighter names, raw sportsbook/odds payload, candidate matches, reason, reviewed flag, reviewer metadata, and timestamps.

Line kind and timestamp semantics:
- For the discovered FightOdds `EventOddsQuery`, import `odds` as `line_kind = 'source_current'` and `oddsPrev` as `line_kind = 'source_previous'` when present.
- `scraped_at` is always the importer observation time.
- `market_timestamp` is null unless the source provides a real market observation timestamp.
- `market_timestamp_semantics` records the meaning explicitly, such as `source_current_at_scrape`, `source_previous_unknown_time`, or a future documented value like `closing_line`.
- Do not label FightOdds rows as open, close, or historical snapshots unless a source endpoint or documentation exposes that meaning.

Odds normalization:
- Store raw American odds and derived decimal/implied values together.
- Positive American odds: `decimal = 1 + american / 100`, `implied_probability = 100 / (american + 100)`.
- Negative American odds: `decimal = 1 + 100 / abs(american)`, `implied_probability = abs(american) / (abs(american) + 100)`.

Production prediction boundary:
- The importer must not write FightOdds historical rows into `odds_snapshots`.
- Existing live odds ingestion and production prediction serving remain unchanged.
- Odds-aware evaluation joins historical odds tables to canonical fights offline and writes reports/evidence only, not active model versions or live prediction rows.
