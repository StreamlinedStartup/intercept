# Locked Over 2.5 Validation Recommendation

Generated from `configs/experiments/over-2-5-locked-validation-v1.json` and `data/experiments/harness/over-2-5-locked-validation-v1.*`.

## Decision

Promote `locked_over_2_5_positive_log_c1_conf58` to a report-only market indicator.

Do not activate automated betting. The candidate cleared the current locked-style historical holdout, but it still needs live forward tracking before production betting recommendations.

## Evidence

| Check | Result |
|---|---:|
| Holdout | Last 35 eligible events |
| Holdout dates | 2024-02-10 through 2026-05-09 |
| Model-eligible fights | 358 |
| Selected model rows | 229 |
| Over 2.5 market rows | 316 |
| Over 2.5 market coverage | 88.3% |
| Model ROI | +33.3% |
| Selected market ROI | +11.4% |
| ROI delta vs market | +21.9% |
| Log-loss delta vs market | -0.0363 |
| Brier delta vs market | -0.0184 |
| Gate result | Passed |

## Interpretation

This is the strongest market-aware prop signal found so far. It did not just show simulated ROI; it beat the selected market baseline on ROI, log loss, and Brier score while clearing the harness stability threshold.

The signal should be treated as an Over 2.5 opportunity indicator when the model probability clears the frozen `0.58` threshold. It is not a generic winner model and should not be generalized to other round totals, finish props, KO/TKO, or submission.

## Next Action

Build a report-only indicator that surfaces:

- `over_2_5_candidate`: true when the frozen model selection policy fires.
- model probability for Over 2.5.
- market no-vig probability for Over 2.5.
- model edge over market.
- status text: `locked validation passed; live tracking required`.

Keep it out of automated bet placement. Track future events and require another forward-only review before labeling it production-active.
