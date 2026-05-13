# Expanded Corpus Winner Validation

The original gate-clearing candidate survived broader corpus windows, and the expanded selected-fight search found more winners.

## Frozen Winner Retest

Candidate:

`log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63`

| Min train samples | Eligible events | Eligible fights | Selected fights | ROI delta | Log-loss delta | Brier delta | Clears gate |
|---:|---:|---:|---:|---:|---:|---:|---|
| 20 | 49 | 462 | 268 | +2.74% | -0.0126 | -0.0062 | true |
| 40 | 46 | 438 | 251 | +2.08% | -0.0115 | -0.0057 | true |
| 60 | 44 | 419 | 234 | +2.23% | -0.0030 | -0.0021 | true |
| 80 | 42 | 397 | 217 | +3.38% | -0.0014 | -0.0015 | true |
| 100 | 40 | 379 | 204 | +2.49% | -0.0011 | -0.0015 | true |

The broader `min_train_samples=20` window covers 49 events and 462 model-eligible fights. The frozen winner selected 268 of those fights and still cleared ROI, log-loss, Brier, and coverage gates.

## Additional Winners

The expanded selected-fight search evaluated 7,777 variants at `min_train_samples=20` and found 150 gate-clearing variants.

| Feature set | Clearing variants | Best variant |
|---|---:|---|
| `production_plus_all_research_market_context` | 67 | `log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66` |
| `production_plus_market_context` | 83 | `log_marketctx_c1p0_temp2p4_blend60_min_confidence0p66` |

Top variant:

| Variant | Events | Selected fights | ROI delta | Log-loss delta | Brier delta | ROI |
|---|---:|---:|---:|---:|---:|---:|
| `log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66` | 48 | 228 | +3.67% | -0.0231 | -0.0107 | 18.0% |

## Recommendation

Keep all candidates `research_only`. Do not write `model_versions`.

The next step is a locked evaluation slice with:

1. The original frozen winner.
2. The top additional winner.
3. A small family of near-identical additional winners only if the locked protocol defines them before evaluation starts.

Do not tune on the locked evaluation results.

## Evidence

- `data/experiments/harness/winner-expanded-corpus-summary.json`
- `data/experiments/harness/winner-expanded-corpus-summary.md`
- `data/experiments/harness/additional-winner-search-summary.json`
- `data/experiments/harness/additional-winner-search-summary.md`
