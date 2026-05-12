# Pre-Fight Signal Catalog

The source of truth for the current signal candidates is `data/experiments/pre-fight-signal-candidates.json`.

The previously recommended report-only experiment, `opponent_adjusted_recent_performance_v1`, has now been evaluated and did not clear the market gate. See `docs/opponent_adjusted_recent_performance_v1.md`.

The next existing-DB candidate, `style_matchup_pressure_v1`, has also been evaluated and did not clear the market gate. See `docs/style_matchup_pressure_v1.md`.

Why this is the next slice:

- Mass search found no edge from the existing feature families.
- Residual reports show the dominant failure is market-prior gap.
- Availability flags were already tested and failed probability-quality gates.
- Opponent-adjusted recent performance adds new pre-fight context using existing DB data before requiring new external sources.

Do not promote any signal from this catalog without a locked market-gated evaluation.
