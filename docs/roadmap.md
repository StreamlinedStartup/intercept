# Roadmap

## Milestone: UFC Fight Predictor v1 ([intercept-7c8e](.beans/intercept-7c8e--ufc-fight-predictor-v1.md))

> Ship v1: Postgres+Timescale schema, on-demand ufcstats fighter backfill, the-odds-api moneyline odds, XGBoost model with point-in-time features, predictions on /upcoming + /predictions track-record...

### Epic: Phase 0: Postgres + TimescaleDB + Drizzle schema ([intercept-3fqo](.beans/intercept-3fqo--phase-0-postgres-timescaledb-drizzle-schema.md))

> Stand up DB layer. 9 tables. Hypertables on timeseries. Fail loud at API startup if DATABASE_URL missing. Reference: docs/ufc-fight-predictor-plan.md#phase-0.


- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-I: Phase 0 verification + close epic ([intercept-aihq](.beans/intercept-aihq--0-i-phase-0-verification-close-epic.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-B: packages/db skeleton (package.json + drizzle config) ([intercept-dvmr](.beans/intercept-dvmr--0-b-packagesdb-skeleton-packagejson-drizzle-config.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-C: Schema for events + fighters (the smallest pair) ([intercept-dwtm](.beans/intercept-dwtm--0-c-schema-for-events-fighters-the-smallest-pair.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-D: client.ts + migrate.ts runner ([intercept-ittn](.beans/intercept-ittn--0-d-clientts-migratets-runner.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-G: Convert timeseries tables to TimescaleDB hypertables ([intercept-jigh](.beans/intercept-jigh--0-g-convert-timeseries-tables-to-timescaledb-hyper.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-E: Round-trip smoke test (the slice closes here) ([intercept-nuwf](.beans/intercept-nuwf--0-e-round-trip-smoke-test-the-slice-closes-here.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-Sm: Smoke gate (agent-browser) ([intercept-o6xw](.beans/intercept-o6xw--0-sm-smoke-gate-agent-browser.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-H: Wire DATABASE_URL into apps/api startup (fail loud) ([intercept-p686](.beans/intercept-p686--0-h-wire-database-url-into-appsapi-startup-fail-lo.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-A: docker-compose up Postgres+Timescale, smoke connect ([intercept-tmtz](.beans/intercept-tmtz--0-a-docker-compose-up-postgrestimescale-smoke-conn.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 0-F: Add remaining tables to schema ([intercept-yiny](.beans/intercept-yiny--0-f-add-remaining-tables-to-schema.md))
### Epic: Phase 1: On-demand fighter backfill ([intercept-1shv](.beans/intercept-1shv--phase-1-on-demand-fighter-backfill.md))

> Per-fighter backfill from /upcoming UI. State machine: none|current|stale_count|stale_stats|in_progress|failed. In-process worker (no scheduler). Admin seed buttons.


- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-H: Admin seed: PPVs only (last 5y) ([intercept-24mz](.beans/intercept-24mz--1-h-admin-seed-ppvs-only-last-5y.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-Sm: Smoke gate (agent-browser) ([intercept-5cmh](.beans/intercept-5cmh--1-sm-smoke-gate-agent-browser.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-J: Phase 1 verification + close epic ([intercept-bgxt](.beans/intercept-bgxt--1-j-phase-1-verification-close-epic.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-F: Compare-sheet integration (corner cells show backfill state) ([intercept-ftr2](.beans/intercept-ftr2--1-f-compare-sheet-integration-corner-cells-show-ba.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-G: Admin seed: in-window cards (smallest) ([intercept-g6vf](.beans/intercept-g6vf--1-g-admin-seed-in-window-cards-smallest.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-C: UI badge on event-fight-card showing state + Load button ([intercept-g7uh](.beans/intercept-g7uh--1-c-ui-badge-on-event-fight-card-showing-state-loa.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-B: fighter_backfill_state row written + GET state route ([intercept-mlyq](.beans/intercept-mlyq--1-b-fighter-backfill-state-row-written-get-state-r.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-E: Stale-count detection in event-fight-card ([intercept-q4n3](.beans/intercept-q4n3--1-e-stale-count-detection-in-event-fight-card.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-I: Admin seed: all UFC (last 5y) ([intercept-t04p](.beans/intercept-t04p--1-i-admin-seed-all-ufc-last-5y.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-D: Async worker + job_id polling ([intercept-vsbt](.beans/intercept-vsbt--1-d-async-worker-job-id-polling.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 1-A: Synchronous backfill route for one fighter (THE SLICE) ([intercept-vuac](.beans/intercept-vuac--1-a-synchronous-backfill-route-for-one-fighter-the.md))
### Epic: Phase 2: odds-mma domain plugin ([intercept-8gxf](.beans/intercept-8gxf--phase-2-odds-mma-domain-plugin.md))

> domains/odds-mma proxying the-odds-api.com (free 500/mo, 5/min). 1h cache. Daily snapshot to odds_snapshots. Fuzzy-match into events/fighters; unmatched logged.


- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-F: Phase 2 verification + close epic ([intercept-1fhe](.beans/intercept-1fhe--2-f-phase-2-verification-close-epic.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-A: domain scaffold + cache copy ([intercept-9bfq](.beans/intercept-9bfq--2-a-domain-scaffold-cache-copy.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-D: Fuzzy-match odds rows to our events/fighters ([intercept-nbi6](.beans/intercept-nbi6--2-d-fuzzy-match-odds-rows-to-our-eventsfighters.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-Sm: Smoke gate (agent-browser) ([intercept-qjks](.beans/intercept-qjks--2-sm-smoke-gate-agent-browser.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-B: GET /api/odds-mma/upcoming (THE SLICE — proxy real call) ([intercept-qsy0](.beans/intercept-qsy0--2-b-get-apiodds-mmaupcoming-the-slice-proxy-real-c.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-C: Snapshot endpoint writes to odds_snapshots ([intercept-vjvz](.beans/intercept-vjvz--2-c-snapshot-endpoint-writes-to-odds-snapshots.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 2-E: Document daily snapshot operation ([intercept-zfc6](.beans/intercept-zfc6--2-e-document-daily-snapshot-operation.md))
### Epic: Phase 3: Python ML extension (XGBoost) ([intercept-at4c](.beans/intercept-at4c--phase-3-python-ml-extension-xgboost.md))

> Extend services/python/worker.py with ml.train, ml.predict, ml.list_models. Point-in-time features (no leakage). Chronological 80/20 split. Save models + metrics to model_versions.


- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-E: Add stance interaction features ([intercept-84gp](.beans/intercept-84gp--3-e-add-stance-interaction-features.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-I: Damage proxy + SHAP integration ([intercept-azd1](.beans/intercept-azd1--3-i-damage-proxy-shap-integration.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-C: train.py — chronological split + first model ([intercept-brce](.beans/intercept-brce--3-c-trainpy-chronological-split-first-model.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-J: Phase 3 verification + close epic ([intercept-elww](.beans/intercept-elww--3-j-phase-3-verification-close-epic.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-F: Add experience features (UFC fight count + ufc_debut) ([intercept-n40x](.beans/intercept-n40x--3-f-add-experience-features-ufc-fight-count-ufc-de.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-H: Add weight class features + finish rate + time in cage ([intercept-nk4h](.beans/intercept-nk4h--3-h-add-weight-class-features-finish-rate-time-in.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-D: predict.py + JSON-RPC handlers in worker.py ([intercept-opm3](.beans/intercept-opm3--3-d-predictpy-json-rpc-handlers-in-workerpy.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-G: Add recent form features (rolling windows) ([intercept-palv](.beans/intercept-palv--3-g-add-recent-form-features-rolling-windows.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-B: features.py — minimal feature set with leakage test (THE SLICE) ([intercept-pcuc](.beans/intercept-pcuc--3-b-featurespy-minimal-feature-set-with-leakage-te.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 3-A: requirements.txt + ml/db.py ([intercept-y3xz](.beans/intercept-y3xz--3-a-requirementstxt-mldbpy.md))
### Epic: Phase 4: Predict API + dashboard UI ([intercept-di4c](.beans/intercept-di4c--phase-4-predict-api-dashboard-ui.md))

> Surface predictions: chip per fight row in /upcoming, win-prob bars + research-only market edge in compare-sheet, /predictions page (table + simulated ROI + calibration), /admin/predict-train retrain.


- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-A: GET /api/predict/fight/:id (model only, THE SLICE) ([intercept-1ved](.beans/intercept-1ved--4-a-get-apipredictfightid-model-only-the-slice.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-H: /predictions simulated ROI cumulative chart ([intercept-33qk](.beans/intercept-33qk--4-h-predictions-roi-cumulative-chart.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-B: Prediction chip on /upcoming fight rows (visual slice closes) ([intercept-a5wm](.beans/intercept-a5wm--4-b-prediction-chip-on-upcoming-fight-rows-visual.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-J: POST /api/predict/train + /admin/predict-train page ([intercept-c5rs](.beans/intercept-c5rs--4-j-post-apipredicttrain-adminpredict-train-page.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-K: Phase 4 verification + ship ([intercept-g0wt](.beans/intercept-g0wt--4-k-phase-4-verification-ship.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-E: GET /api/predict/event/:id (batch) ([intercept-g4oo](.beans/intercept-g4oo--4-e-get-apipredicteventid-batch.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-G: /predictions page — track record table ([intercept-ifp6](.beans/intercept-ifp6--4-g-predictions-page-track-record-table.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-Sm: Smoke gate (agent-browser) ([intercept-j39k](.beans/intercept-j39k--4-sm-smoke-gate-agent-browser.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-F: GET /api/predict/history (track-record query) ([intercept-lmh6](.beans/intercept-lmh6--4-f-get-apipredicthistory-track-record-query.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-D: Edge calculation joining odds_snapshots ([intercept-oakk](.beans/intercept-oakk--4-d-edge-calculation-joining-odds-snapshots.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-C: Win-prob bars in compare-sheet ([intercept-pct4](.beans/intercept-pct4--4-c-win-prob-bars-in-compare-sheet.md))
- ![task](https://img.shields.io/badge/task-1d76db?style=flat-square) 4-I: /predictions calibration histogram ([intercept-qtw9](.beans/intercept-qtw9--4-i-predictions-calibration-histogram.md))
