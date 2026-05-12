# Market Experiment Harness

The harness runs report-only UFC predictor experiments from checked-in JSON config. It exists to make model-family, feature-transform, and market-blend comparisons fast and repeatable without writing active `model_versions`.

## Contract

- Config schema: `configs/experiments/market-experiment.schema.json`
- Example matrix: `configs/experiments/market-grid.example.json`
- Corpus source: matched market-covered UFC fights.
- Market baseline: no-vig FightOdds consensus market favorite.
- Split policy: chronological walk-forward; each evaluated event trains only on prior market-covered fights.
- Output status: `research_only`.
- Persistence: JSON/Markdown artifacts only; no model files and no `model_versions` writes.

## Guardrails

Running many variants can easily overfit the current corpus. The harness therefore separates experiment speed from activation proof:

- Use the current corpus for discovery and ranking.
- Treat any winner as a candidate, not proof.
- Require a locked future evaluation slice before changing product status.
- Require candidate ROI at least +2pp above market favorite.
- Require log loss and Brier not worse than market favorite.
- Flag small-sample winners as unstable instead of promoting them.

MLflow can be layered on later as a tracking UI. The first durable interface is the config file plus the JSON/Markdown run registry because that is easier to review, commit, and reproduce in this repo.
