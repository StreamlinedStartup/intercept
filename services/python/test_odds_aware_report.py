"""Tests for odds-aware report math."""
from __future__ import annotations

import pytest

from ml.odds_aware_report import (
    american_to_implied_probability,
    edge,
    flat_stake_net_profit,
    remove_vig,
)


def test_american_odds_to_implied_probability() -> None:
    assert american_to_implied_probability(-150) == pytest.approx(0.6)
    assert american_to_implied_probability(200) == pytest.approx(1 / 3)


def test_no_vig_normalization() -> None:
    left, right = remove_vig(0.6, 0.5)

    assert left == pytest.approx(0.5454545)
    assert right == pytest.approx(0.4545454)
    assert left + right == pytest.approx(1.0)


def test_model_edge_is_model_probability_minus_market_probability() -> None:
    assert edge(0.58, 0.52) == pytest.approx(0.06)
    assert edge(0.45, 0.52) == pytest.approx(-0.07)


def test_flat_stake_profit_math() -> None:
    assert flat_stake_net_profit(2.5, True) == pytest.approx(1.5)
    assert flat_stake_net_profit(1.7, False) == pytest.approx(-1.0)
