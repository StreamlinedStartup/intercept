# Odds-Aware Evaluation

- Source events imported: 3
- Source events matched: 1
- Source fights imported: 46
- Source fights matched: 12
- Moneyline rows imported: 2173
- Moneyline rows linked to canonical fighters: 600
- Scored events: 1
- Scored fights: 12
- Model-edge ROI: -100.0%
- Market-favorite ROI: 31.4%

## Timestamp And CLV

FightOdds source_current lines are captured at import scrape time. Use them as close/current market consensus only. FightOdds source_previous lines do not include timestamps, so closing-line value is not reported.

## ROI

| Strategy | Bets | Wins | Net profit | ROI |
|---|---:|---:|---:|---:|
| Model edge | 6 | 0 | -6.0000 | -100.0% |
| Market favorite | 12 | 10 | 3.7733 | 31.4% |

## Confidence Buckets

| Bucket | Count | Accuracy | ROI |
|---|---:|---:|---:|
| 50-55 | 7 | 28.6% | -64.0% |
| 55-60 | 2 | 100.0% | 13.9% |
| 60-65 | 3 | 33.3% | -51.3% |

## Edge Buckets

| Bucket | Count | Accuracy | ROI |
|---|---:|---:|---:|
| negative | 6 | 83.3% | 4.4% |
| 10+ | 1 | 0.0% | -100.0% |
| 2-5 | 2 | 0.0% | -100.0% |
| 5-10 | 3 | 0.0% | -100.0% |

## Market Calibration

- Market favorite accuracy: 83.3%
- Average market favorite no-vig probability: 65.0%
- Calibration gap: +18.3%

## Secondary Model Metrics

| Accuracy | Log loss | Brier | ROC AUC |
|---:|---:|---:|---:|
| 0.4167 | 0.7087 | 0.2576 | 0.4571 |

## Source Coverage

| Source event | Canonical event | Status | Source fights | Matched fights | Moneylines | Linked moneylines |
|---|---|---|---:|---:|---:|---:|
| 5362 UFC Fight Night 237: Moreno vs. Royval 2 | 902ab9197b83d0db | matched | 14 | 12 | 652 | 600 |
| 5318 UFC Fight Night 238: Rozenstruik vs. Gaziev |  | unmatched | 16 | 0 | 688 | 0 |
| 5356 UFC 299: O'Malley vs. Vera 2 |  | unmatched | 16 | 0 | 833 | 0 |

## Recommendation

FightOdds remains the best discovered historical source because it exposes stable event IDs, GraphQL event pagination, sportsbook-level moneylines, and repeatable direct HTTP access. Current limitation is canonical matching coverage, not source availability.

## Smoke Gate

This epic added DB/Python research commands and generated artifacts only; no HTTP route or UI surface was added.
