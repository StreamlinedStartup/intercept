# Prediction Interpretation Guide

This guide explains how to read UFC Fight Predictor outputs without confusing a straight-up pick with betting value.

## Core Terms

### Model Win Probability

The model win probability is the model's estimate that a fighter wins the fight.

Example:

| Fighter | Model probability |
|---|---:|
| Khamzat Chimaev | 57.94% |
| Sean Strickland | 42.06% |

The model's straight-up pick is the fighter above 50%. In this example, the pick is Chimaev.

### Confidence

Confidence is the winning side's distance from 50%.

```text
confidence = max(model_prob, 1 - model_prob)
model_edge_over_coin_flip = confidence - 50%
```

For a 57.94% pick:

```text
confidence = 57.94%
model_edge_over_coin_flip = 7.94 percentage points
```

That is a modest lean, not a lock.

### Market Implied Probability

American odds can be converted into the break-even probability required for a bet to be fair.

For positive odds:

```text
implied_probability = 100 / (odds + 100)
```

For negative odds:

```text
implied_probability = abs(odds) / (abs(odds) + 100)
```

Examples:

| Odds | Break-even probability |
|---:|---:|
| +500 | 16.67% |
| +200 | 33.33% |
| +100 | 50.00% |
| -150 | 60.00% |
| -300 | 75.00% |

When both sides have odds, remove the sportsbook hold by normalizing both implied probabilities before calculating model-vs-market edge.

### Model-vs-Market Edge

Edge compares the model's probability for a fighter against the market's implied probability.

```text
edge = model_probability - market_probability
```

If Strickland is +500:

```text
market_probability = 16.67%
model_probability = 42.06%
edge = +25.39 percentage points
```

This means the model still picked Chimaev, but Strickland was the value side at that price.

## Pick vs Value

The model can pick one fighter while the value side is the other fighter.

Example:

| Fighter | Model probability | Market probability | Interpretation |
|---|---:|---:|---|
| Chimaev | 57.94% | much higher than 57.94% if heavily favored | Pick, but likely overpriced |
| Strickland | 42.06% | 16.67% at +500 | Underdog value |

The straight-up pick asks:

> Who is more likely to win?

The value question asks:

> Is the market price too high or too low relative to the model?

Those are different questions.

## Expected Value

Expected value estimates the long-run return if the model probability is correct.

For a +500 underdog, a $1 stake wins $5 profit if the fighter wins and loses $1 if the fighter loses.

```text
EV = (model_probability * profit_if_win) - ((1 - model_probability) * stake)
```

For Strickland at +500 with a 42.06% model probability:

```text
EV = (0.4206 * 5) - (0.5794 * 1)
EV = 2.1030 - 0.5794
EV = +1.5236 per $1 risked
```

That is a theoretical +152.36% expected ROI. Treat this as a signal to investigate, not proof of a profitable bet. The model must be calibrated across many fights before this number can be trusted.

## Threshold Bands

Use probability and edge bands as review categories, not automatic betting rules.

### Pick Confidence

| Model pick probability | Label | Interpretation |
|---:|---|---|
| 50-55% | Toss-up lean | Very fragile. Do not overread. |
| 55-60% | Small lean | Useful for ranking fights, weak as a standalone signal. |
| 60-65% | Moderate lean | Worth reviewing feature drivers and market agreement. |
| 65-70% | Strong lean | Meaningful only if calibration confirms this bucket wins near that rate. |
| 70%+ | Very strong lean | Rare; inspect for data leakage, stale inputs, or missing context. |

### Market Edge

| Model edge vs market | Label | Interpretation |
|---:|---|---|
| 0-2 percentage points | Noise | Too small for normal model/market error. |
| 2-5 percentage points | Watchlist | Track, but usually below action threshold. |
| 5-10 percentage points | Possible value | Candidate for review if model inputs look sane. |
| 10+ percentage points | Large value gap | Investigate carefully; could be real, or could expose model/data weakness. |
| 20+ percentage points | Extreme gap | Assume something needs review before trusting it. |

The current UI already uses edge filters such as `>5%` and `>10%`. Those should remain evaluation thresholds, not automatic bet instructions.

## Calibration Comes First

A model is useful only if its probabilities are calibrated.

If the model says 65% across 100 comparable predictions, those picks should win about 65 times. If they win 52 times, the model may still rank fighters decently, but its probabilities are too confident.

Track:

- accuracy by confidence bucket;
- log loss;
- Brier score;
- ROC AUC;
- ROI by edge bucket when pre-event odds are available;
- live prediction history where the prediction was saved before the result.

Do not judge the model from one fight. A single upset can be a good value signal and still lose.

## Operator Rules

- Do not call a 55-60% pick a strong prediction.
- Do not treat the picked fighter as the bet side without comparing market price.
- Do not calculate ROI from odds unless those odds existed before the simulated fight date.
- Do not trust a large underdog edge until the fighter IDs, recent fight history, and feature drivers look sane.
- Do not promote a model change because of one correct upset or one wrong favorite.
- Prefer walk-forward results and saved live predictions over hand-picked examples.
