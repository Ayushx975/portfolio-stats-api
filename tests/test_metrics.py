"""Unit tests for the metrics engine."""
import math

from app.services import metrics


def test_cagr_positive_growth():
    # 100 -> 121 over ~1 year => ~21% CAGR
    v = metrics.cagr(100, 121, 365)
    assert math.isclose(v, 21.0, abs_tol=1.0)


def test_cagr_loss():
    assert metrics.cagr(100, 50, 365) < 0


def test_daily_returns_basic():
    assert metrics.daily_returns([100, 110, 99]) == [0.1, -0.1]


def test_volatility_zero_for_flat():
    assert metrics.volatility_pct([0.01, 0.01, 0.01]) == 0.0


def test_volatility_positive_for_mixed():
    assert metrics.volatility_pct([0.01, -0.02, 0.03, -0.01]) > 0


def test_sharpe_flat_returns_zero():
    assert metrics.sharpe([0.01, 0.01]) == 0.0


def test_sortino_needs_downside():
    # all-positive returns => no downside deviation => 0 by convention
    assert metrics.sortino([0.01, 0.02, 0.015]) == 0.0


def test_max_drawdown():
    series = [100, 120, 90, 130]
    # peak 120 -> trough 90 = -25%
    assert math.isclose(metrics.max_drawdown_pct(series), -25.0, abs_tol=0.001)


def test_max_drawdown_all_up():
    assert metrics.max_drawdown_pct([1, 2, 3, 4]) == 0.0


def test_herfindahl_single_asset():
    assert metrics.herfindahl_score([100.0]) == 0.0


def test_herfindahl_equal_split():
    n = 4
    score = metrics.herfindahl_score([25.0] * n)
    assert score == 1.0


def test_herfindahl_between():
    score = metrics.herfindahl_score([70.0, 30.0])
    assert 0.0 < score < 1.0


def test_interpret_labels():
    assert metrics.interpret(0.9) == "well diversified"
    assert metrics.interpret(0.5) == "moderately diversified"
    assert metrics.interpret(0.1) == "concentrated"
