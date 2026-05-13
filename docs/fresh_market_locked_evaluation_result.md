# Fresh Market Locked Evaluation Result

The frozen candidates did not clear the fresh post-holdout market gate.

## Fresh Slice

- Type: imported FightOdds UFC events after `2024-03-09`
- Date range scored: `2025-08-16` to `2026-05-09`
- Events: 30
- Model-eligible fights: 304
- Value status: `research_only`
- Writes `model_versions`: `false`

## Results

| Candidate | Selected fights | ROI | ROI delta | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---:|---:|---|
| `original_winner_allresearch_c2p5_temp2p2_blend45_conf63` | 164 | -3.2% | +0.0% | 0.0129 | 0.0045 | false |
| `top_additional_allresearch_c2p0_temp2p2_blend55_conf66` | 129 | -2.4% | +0.0% | 0.0147 | 0.0046 | false |
| `top_marketctx_c1p0_temp2p4_blend60_conf66` | 115 | -1.6% | +0.0% | 0.0211 | 0.0066 | false |

Market favorite on the full fresh slice scored 304 fights with 70.4% accuracy,
0.5885 log loss, 0.2017 Brier, and 2.8% simulated research ROI.

## Interpretation

The frozen winners from the current-corpus search did not transfer to the fresh
post-holdout market slice. They selected higher-accuracy subsets, but those
subsets did not beat the selected-fight market baseline and had worse probability
quality than market.

Do not promote these candidates. Further search is research-only and needs a new
future lock before any activation claim.
