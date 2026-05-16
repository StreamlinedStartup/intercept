# Locked Evaluation Result

The frozen candidates did not clear the last-10-event historical locked-style holdout.

## Holdout

- Type: last 10 chronological market-covered events
- Date range: 2023-12-09 to 2024-03-09
- Events: 10
- Fights: 104

## Results

| Candidate | Events | Selected fights | ROI | ROI delta | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---:|---:|---:|---|
| `original_winner_allresearch_c2p5_temp2p2_blend45_conf63` | 10 | 59 | 6.7% | 0.0% | 0.0182 | 0.0065 | false |
| `top_additional_allresearch_c2p0_temp2p2_blend55_conf66` | 9 | 49 | 4.6% | 0.0% | 0.0219 | 0.0080 | false |
| `top_marketctx_c1p0_temp2p4_blend60_conf66` | 9 | 37 | 0.6% | 0.0% | 0.0312 | 0.0112 | false |

All three candidates failed the ROI delta gate, probability-quality gates, and coverage gate.

## Interpretation

This invalidates promotion from the current corpus. The broader search still found useful signal families, but the frozen candidates did not survive the held-out historical slice.

Do not tune around this holdout. The next valid step is importing fresh market-covered events and evaluating the frozen candidates on genuinely new data.

Keep everything `research_only`; do not write `model_versions`.
