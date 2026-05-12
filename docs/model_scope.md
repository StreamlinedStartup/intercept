# UFC Fight Predictor Model Scope

This document explains what the current model does, what it does not do, how to read its feature rankings, and how we should backtest it. It is written for product and operator review, not for statisticians.

## What The Model Answers

The model answers one narrow question:

> Given Fighter A, Fighter B, and the fight date, which fighter is more likely to win?

It returns:

- `predicted_winner_id`: the fighter it thinks is more likely to win.
- `win_prob`: the model's estimated chance for the predicted winner.
- `model_version`: the trained model file used.
- `contributing_features`: the top reasons that moved this specific prediction up or down.

The model is not trying to predict method of victory, round, over/under, prop bets, or live in-fight outcomes.

## Current Model Type

The current model is an XGBoost classifier. In plain English, it is a collection of small decision trees that learn patterns from historical fights.

It is useful here because:

- It handles missing data without us pretending unknown values are zero.
- It can learn non-linear patterns, like "a layoff matters more for some fighter profiles than others."
- It gives feature-importance and per-prediction contribution data so we can inspect why it made a pick.

The model trains only on completed fights that have exactly two win/loss result rows.

## How Training Avoids Cheating

Every feature is built point-in-time.

For a target fight on June 1, 2026, the feature builder only uses fights with event dates before June 1, 2026. It does not look at the target fight result, later fights, later stats, or later odds.

Training also uses a chronological split:

- The oldest 80% of labeled fights train the model.
- The newest 20% are held out for validation.

That matters. A random split would let future fighting history leak backward into the training set and would make the model look stronger than it really is.

## Current Latest Model Snapshot

Latest local model row at the time this doc was written:

| Field | Value |
|---|---:|
| Model version | `20260511T134646095031Z` |
| Training samples | 8,538 |
| Holdout accuracy | 61.24% |
| Log loss | 0.655 |
| Brier score | 0.232 |
| ROC AUC | 0.655 |

Interpretation:

- Accuracy says how often the model picked the winner on the holdout set.
- Log loss and Brier score say whether the probabilities are sensible, not just whether the pick was right.
- ROC AUC says how well the model ranks stronger picks above weaker picks. The current value is modest, so we should avoid over-trusting the model until the training set is larger.

Compared with the previous external-corpus model, `20260511T011334074447Z`, the Decision Engine v2 core-signal retrain changed the holdout metrics by:

| Metric | Previous | Current | Delta |
|---|---:|---:|---:|
| Accuracy | 60.42% | 61.24% | +0.82 pp |
| Log loss | 0.658 | 0.655 | -0.003 |
| Brier score | 0.233 | 0.232 | -0.001 |
| ROC AUC | 0.648 | 0.655 | +0.007 |

This is still an early model. Treat the numbers as a working baseline, not as proof of a durable betting edge.

See `docs/model_reliability_policy.md` for the current `value_status` policy. As of the D2-RV final report, the product status is `insufficient_coverage`: market comparisons and ROI remain simulated research outputs until the coverage and market-gate criteria pass.

## Features The Model Uses

Most numeric features are directional. A `_diff` feature means Fighter A minus Fighter B.

Example: `reach_diff = 3` means Fighter A has a 3 inch reach advantage. `reach_diff = -3` means Fighter B has the 3 inch reach advantage.

### Career Stats

These summarize each fighter's career-to-date performance before the target fight:

| Feature | Plain-English Meaning |
|---|---|
| `slpm_diff` | Significant strikes landed per minute advantage |
| `str_acc_diff` | Striking accuracy advantage |
| `sapm_diff` | Significant strikes absorbed per minute difference |
| `str_def_diff` | Striking defense advantage |
| `td_avg_diff` | Takedowns landed per 15 minutes advantage |
| `td_acc_diff` | Takedown accuracy advantage |
| `td_def_diff` | Takedown defense advantage |
| `sub_avg_diff` | Submission attempts per 15 minutes advantage |

### Physical Profile

| Feature | Plain-English Meaning |
|---|---|
| `height_diff` | Height advantage in inches |
| `reach_diff` | Reach advantage in inches |
| `age_diff` | Age difference on fight date |

### UFC Experience

| Feature | Plain-English Meaning |
|---|---|
| `ufc_fight_count_a` | Fighter A's prior UFC fights |
| `ufc_fight_count_b` | Fighter B's prior UFC fights |
| `ufc_fight_count_diff` | UFC experience advantage |
| `ufc_debut` | Whether either fighter is making a UFC debut |

This intentionally counts UFC fights only. Prior Bellator, Strikeforce, or other promotion fights may exist in career stats, but they do not count as UFC experience.

### Recent Form

| Feature | Plain-English Meaning |
|---|---|
| `wins_last_3_diff` | Recent win advantage across the last 3 fights |
| `wins_last_5_diff` | Recent win advantage across the last 5 fights |
| `loss_streak_a` | Fighter A's active losing streak before the fight |
| `loss_streak_b` | Fighter B's active losing streak before the fight |
| `coming_off_loss_a` | Fighter A lost their previous fight |
| `coming_off_loss_b` | Fighter B lost their previous fight |
| `days_since_last_fight_a` | Fighter A's layoff length in days |
| `days_since_last_fight_b` | Fighter B's layoff length in days |
| `days_since_last_fight_diff` | Layoff difference |
| `long_layoff_a` | Fighter A has been out more than 365 days |
| `long_layoff_b` | Fighter B has been out more than 365 days |

### Weight Class And Fight Style

| Feature | Plain-English Meaning |
|---|---|
| `weight_class_change` | Either fighter changed weight class from their most recent fight |
| `same_weight_class_count_diff` | Experience advantage in this exact weight class |
| `finish_rate_diff` | Advantage in winning by KO/TKO/submission |
| `decision_rate_diff` | Advantage in winning by decision |
| `time_in_cage_a` | Fighter A's total prior cage time in seconds |
| `time_in_cage_b` | Fighter B's total prior cage time in seconds |

### Decision Engine v2 Core Signals

| Feature | Plain-English Meaning |
|---|---|
| `avg_ending_round_diff` | Prior average ending-round difference |
| `decision_tendency_diff` | Prior decision-rate difference |
| `late_round_exposure_diff` | Prior late-round exposure difference |
| `common_opponent_count` | Number of shared prior opponents before the target fight |
| `common_opponent_win_diff` | Fighter A wins minus Fighter B wins against shared prior opponents |

The API also returns these as readable `decision_signals` for the compare sheet. Those labels are review signals, not betting instructions.

### Damage Proxy

| Feature | Plain-English Meaning |
|---|---|
| `damage_index_a` | Recent significant strikes absorbed by Fighter A, with KO/TKO losses weighted heavier |
| `damage_index_b` | Recent significant strikes absorbed by Fighter B, with KO/TKO losses weighted heavier |

This is not an injury report. It is a rough proxy for recent punishment.

### Stance Matchup

The model uses one stance feature at a time:

| Feature | Plain-English Meaning |
|---|---|
| `stance_orthodox_orthodox` | Orthodox vs orthodox |
| `stance_orthodox_southpaw` | Fighter A orthodox, Fighter B southpaw |
| `stance_southpaw_orthodox` | Fighter A southpaw, Fighter B orthodox |
| `stance_southpaw_southpaw` | Southpaw vs southpaw |
| `stance_switch_involved` | At least one fighter is switch stance |
| `stance_unknown` | Missing or unsupported stance data |

Direction matters. Orthodox vs southpaw is not treated the same as southpaw vs orthodox.

## How Feature Ranking Works

There are two different rankings. They answer different questions.

### Model-Level Feature Importance

Model-level feature importance asks:

> Across the whole training run, which features did the model use most?

The latest local model's top features were:

| Rank | Feature | What It Means |
|---:|---|---|
| 1 | `coming_off_loss_b` | Whether Fighter B lost their previous fight |
| 2 | `loss_streak_b` | Fighter B's active losing streak |
| 3 | `time_in_cage_b` | Fighter B's total prior cage time |
| 4 | `days_since_last_fight_a` | Fighter A's layoff length |
| 5 | `weight_class_change` | Whether either fighter changed weight class |
| 6 | `ufc_fight_count_a` | Fighter A's prior UFC experience |
| 7 | `time_in_cage_a` | Fighter A's total prior cage time |
| 8 | `same_weight_class_count_diff` | Weight-class-specific experience advantage |

Important caveat: model-level importance does not mean "this feature always helps the same fighter." It only says the model found that field useful when splitting historical examples.

### Per-Prediction Contributions

Per-prediction contributions ask:

> For this one fight, what moved the prediction?

The API returns `contributing_features`, each with:

- `name`: the feature.
- `value`: the fight-specific value.
- `shap`: how much that feature moved the model output.

Read `shap` as directional pressure:

- Positive values push toward Fighter A.
- Negative values push toward Fighter B.
- Larger absolute values matter more for that prediction.

If the predicted winner is Fighter B, the same contribution list still uses Fighter A as the reference point. A strongly negative feature can be a major reason Fighter B was picked.

## How Odds Edge Works

When odds are available, the API converts each fighter's decimal odds into a market probability and removes the bookmaker hold by normalizing both sides.

Then:

```text
edge_pct = model_win_prob - market_prob
```

Example:

- Model says a fighter wins 60%.
- Market implies 52%.
- Edge is +8 percentage points.

The current history page treats an edge above 5 percentage points as a simulated one-unit research entry. This is for tracking calibration and market comparison only, not auto-betting or a validated edge claim.

## Backtesting We Can Do Now

There are two useful backtests already supported by the current design.

### 1. Training Holdout Backtest

This happens every time the model trains.

Process:

1. Sort completed fights by event date.
2. Train on the oldest 80%.
3. Test on the newest 20%.
4. Store accuracy, log loss, Brier score, and ROC AUC in `model_versions`.

This answers:

> If we trained on older fights, how well did the model predict newer fights?

This is the right first baseline because it prevents future data from leaking into the past.

Limitations:

- With only 80 local samples, the holdout set is small.
- It tests one time split, not many different eras.
- It does not fully simulate repeated model retraining over time.

### 2. Live Prediction Track Record

Every prediction served by the API is persisted into the `predictions` table with:

- fight id
- model version
- prediction timestamp
- predicted winner
- win probability
- market edge when odds exist

After the fight result is known, `/api/predict/history` can score those saved predictions.

This answers:

> How have our actual served predictions performed?

It tracks:

- pick accuracy
- log loss
- Brier score
- simulated ROI for bets where edge was greater than 5 percentage points

This is the most honest product metric because it only scores predictions that existed before the outcome was known.

### 3. Walk-Forward Backtest

Decision Engine v2 core signals were first checked with a 20-event walk-forward run:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --start-date 2024-01-01 --max-events 20 --min-train-samples 200 --output data/backtests/decision-engine-v2-core-signals.json
```

Result summary:

| Field | Value |
|---|---:|
| Events scored | 20 |
| Predictions scored | 247 |
| Accuracy | 54.25% |
| Log loss | 0.683 |
| Brier score | 0.245 |
| ROC AUC | 0.586 |

That 20-event run is broader than the earlier two-event smoke run in `data/backtests/smoke-walk-forward.json`, but it is still only a smoke/comparison artifact.

The full imported UFC Stats CSV corpus was then evaluated without a `--max-events` cap:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --min-train-samples 200 --output data/backtests/full-corpus-walk-forward.json --progress-every 25
PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/full-corpus-walk-forward.json --output data/backtests/full-corpus-walk-forward.md
```

Policy:

- Start date: no explicit start date. The runner considers every eligible completed UFC event in the imported corpus.
- Training floor: `min_train_samples=200`. Candidate events before that threshold are skipped, so the first scored event is `UFC 22: Only One Can be Champion` on September 24, 1999 with 206 prior training samples.
- Final scored event: `UFC 328: Chimaev vs. Strickland` on May 9, 2026 from the current imported snapshot.
- Odds are not included here. ROI and market-favorite baselines belong to the historical odds source work.

Full-corpus result summary:

| Field | Value |
|---|---:|
| Events scored | 753 |
| Predictions scored | 8,332 |
| Accuracy | 59.35% |
| Average confidence | 59.54% |
| Calibration gap | -0.19 pp |
| Log loss | 0.669 |
| Brier score | 0.238 |
| ROC AUC | 0.627 |

Confidence buckets:

| Confidence | Predictions | Accuracy | Avg confidence | Calibration gap | Log loss | Brier | ROC AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 50-55% | 2,643 | 52.29% | 52.51% | -0.22 pp | 0.692 | 0.250 | 0.524 |
| 55-60% | 2,327 | 58.92% | 57.39% | +1.53 pp | 0.678 | 0.242 | 0.592 |
| 60-65% | 1,703 | 62.54% | 62.41% | +0.13 pp | 0.660 | 0.234 | 0.639 |
| 65-70% | 915 | 66.23% | 67.20% | -0.97 pp | 0.640 | 0.224 | 0.664 |
| 70%+ | 744 | 70.03% | 75.20% | -5.18 pp | 0.618 | 0.213 | 0.706 |

This is a useful model-evaluation baseline: confidence rises mostly monotonically with realized accuracy, and the model is well calibrated overall. The important caveat is the `70%+` bucket. Those picks average 75.20% confidence but land at 70.03%, so the model is over-confident by 5.18 percentage points at the top end.

Implication: we should not simply push more picks into `70%+`. First, improve separation for truly high-certainty fights or apply a calibration/capping layer so the UI does not overstate top-end certainty. Useful next diagnostics are feature-regime calibration slices, especially debut fights, long layoffs, weight-class changes, sparse recent-form histories, and era splits. It is not evidence of betting edge because it does not compare against historical market prices.

## Backtesting We Should Add Next

The stronger backtest is a longer walk-forward backtest with odds-aware scoring.

Plain-English process:

1. Pick a historical starting point, such as January 1, 2024.
2. Train only on fights before that date.
3. Predict the next event.
4. Record the prediction, confidence, market odds, and result.
5. Move forward to the next event.
6. Retrain using all fights known before that next event.
7. Repeat through the historical schedule.

This better simulates how the product would have behaved in real life.

Recommended walk-forward outputs:

- accuracy by month or quarter
- log loss over time
- Brier score over time
- calibration chart
- simulated research ROI by edge bucket, such as 0-2%, 2-5%, 5-10%, and 10%+
- performance by confidence bucket, such as 50-55%, 55-60%, 60-65%, and 65%+
- performance by feature regime, such as debut fights, long-layoff fights, and weight-class-change fights

The key rule: every simulated prediction must use only the data that would have existed before that event.

## What Would Make The Model More Trustworthy

Highest-value improvements:

1. Increase the training corpus. The current 80-sample model is too small for strong conclusions.
2. Add walk-forward backtesting so we can evaluate many historical prediction points.
3. Track calibration by confidence bucket. A useful model needs its 65% picks to win about 65% over time.
4. Compare against baselines:
   - always pick the fighter with more UFC fights
   - always pick the younger fighter
   - always pick the betting favorite
   - always pick the fighter with better implied market probability
5. Report simulated research ROI by edge bucket instead of one global ROI number.

## Known Blind Spots

The current model does not know:

- current injuries
- fight-week illnesses
- camp changes
- coach quality
- weight-cut quality
- short-notice replacement context
- betting line movement
- public news or social sentiment
- method-specific matchup details beyond the current aggregate features

The model can still be useful, but these blind spots are exactly why we should treat predictions as a decision-support signal rather than a final answer.

## Operator Summary

Use the model this way:

- Trust the pick more when model probability, research-only market edge, and top contributing features all make intuitive sense.
- Be skeptical when the model is confident but the top reason is a weak proxy, such as sparse debut data.
- Do not judge the model by one fight. Judge it by calibration, log loss, and simulated ROI across many saved predictions.
- Do not claim a betting edge until leakage audits, baseline comparisons, market coverage, walk-forward backtesting, and live prediction history all support it.
