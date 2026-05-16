# Locked Evaluation Summary

The frozen candidates did not clear the last-10-event historical locked-style holdout.

Holdout:

- Events: 10
- Fights: 104
- Date range: 2023-12-09 to 2024-03-09

| Candidate | Events | Selected fights | ROI | ROI delta | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---:|---:|---:|---|
| `original_winner_allresearch_c2p5_temp2p2_blend45_conf63` | 10 | 59 | 6.7% | 0.0% | 0.0182 | 0.0065 | false |
| `top_additional_allresearch_c2p0_temp2p2_blend55_conf66` | 9 | 49 | 4.6% | 0.0% | 0.0219 | 0.0080 | false |
| `top_marketctx_c1p0_temp2p4_blend60_conf66` | 9 | 37 | 0.6% | 0.0% | 0.0312 | 0.0112 | false |

All candidates failed ROI delta, probability-quality, and coverage gates.

Recommendation: do not promote. The next step is fresh out-of-sample market-covered data, not tuning this holdout after seeing the result.
