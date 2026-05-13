# Locked Evaluation Protocol v1

This protocol freezes the candidate list before running a locked-style historical holdout evaluation.

## Frozen Candidates

1. `original_winner_allresearch_c2p5_temp2p2_blend45_conf63`
2. `top_additional_allresearch_c2p0_temp2p2_blend55_conf66`
3. `top_marketctx_c1p0_temp2p4_blend60_conf66`

The exact model settings are in `configs/experiments/locked-evaluation-candidates-v1.json`.

## Holdout

Use the last 10 chronological market-covered events as the holdout.

Each target event still trains only on fights before that event date. The holdout filter limits which target events are scored; it does not allow future fights into training.

## Interpretation

This is historical locked-style validation, not true future validation. Prior discovery work has already inspected the current corpus, so a pass here is stronger than the prior search results but still not production activation proof.

## Rules

- Do not change candidates after evaluation starts.
- Do not tune on holdout results.
- Keep outputs `research_only`.
- Do not write `model_versions`.
- Compare selected candidates against the market baseline on the same selected fight subset.
