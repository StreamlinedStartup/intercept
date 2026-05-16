# Method and Round Prop Target Recommendation

Generated from `configs/experiments/method-round-prop-targets-v1.json` and `data/experiments/harness/method-round-prop-targets-v1.*`.

## Recommendation

Keep the method/round prop targets in report-only mode and promote exactly one target to locked validation: `over_2_5_positive_log_c1_conf58`.

Do not activate production betting recommendations from this run. The current corpus is a discovery corpus, not a locked future holdout. The next activation gate is a locked validation slice using future events or a fixed chronological holdout that was not used for threshold selection.

## Target Calls

| Target | Call | Evidence | Next action |
|---|---|---|---|
| Over 2.5 rounds | Promote to locked validation | Cleared discovery gate: +21.9% ROI delta vs market, -0.0024 log-loss delta, -0.0057 Brier delta, 450 selected rows, 46.3% market-backed coverage | Run a locked future-slice validation config with no threshold tuning |
| Goes to decision | Keep as market-strength warning only | Model ROI was -2.7%, but selected market-side ROI was +14.8% on 49 entries | Validate whether model-filtered decision rows are a market-strength indicator, not a model bet |
| Finish likelihood | Reject for now | Model ROI -14.2%, selected market ROI -13.9%, worse probability quality than market | Improve method-specific prop coverage and rerun; do not use finish edge |
| KO/TKO | Reject model edge for now | Model ROI -14.8%, worse probability quality than market, unstable coverage | Keep importing fight-level KO metadata; add fighter-specific KO lines only if two-sided coverage improves |
| Submission | Reject model edge for now | Model ROI -15.1%, 66 selected rows, worse probability quality than market, unstable coverage | Keep importing fight-level submission metadata; add fighter-specific submission lines only if two-sided coverage improves |
| Over 1.5 rounds | Reject for now | Positive model ROI (+7.9%) but market side did better (+11.0%) and probability quality was worse | Do not prioritize; revisit after stronger round-total feature work |
| Over 3.5 rounds | Coverage-blocked | +51.1% model ROI, but only 29 market rows / 4.2% coverage and failed log-loss/Brier | Import more books/events with 3.5 round totals before interpreting ROI |
| Over 4.5 rounds | Coverage-blocked despite high ROI | +67.7% model ROI and +46.1% ROI delta, but only 30 market rows / 4.4% coverage and failed log-loss/Brier | Treat as noise until 4.5 round-total coverage is materially larger |

## Data and Import Actions

1. Preserve the current `DISTANCE` and `OVERUNDER_*` imports. These are sufficient for decision, finish, and over/under round labels with market baselines.
2. Keep fight-level method metadata from prop rows for KO/TKO and submission. It gives enough coverage for discovery, but not enough reliability for activation.
3. Do not prioritize single-sided fighter-specific method props until the importer can prove stable two-sided coverage. Sparse single-sided rows will inflate apparent opportunities.
4. Expand historical prop imports before interpreting over 3.5 or over 4.5. Current coverage is roughly 4%, so both are unstable even when simulated ROI is high.

## Operating Policy

- `over_2_5_positive_log_c1_conf58` is a candidate for locked validation, not a deployable betting signal.
- Decision rows may become a market-strength warning, but the model side did not beat the market in this run.
- Finish, KO/TKO, submission, over 1.5, over 3.5, and over 4.5 stay report-only rejects until a future locked validation run clears the same market gate.
