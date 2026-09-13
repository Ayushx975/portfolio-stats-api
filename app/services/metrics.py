"""Pure math for portfolio metrics — no I/O, fully unit-testable."""
from __future__ import annotations

import math

RISK_FREE_DAILY = 0.07 / 252  # ~7% annual on 252 trading days


def cagr(begin: float, end: float, days: int) -> float:
    if begin <= 0 or days <= 0:
        return 0.0
    years = days / 365.0
    if end <= 0:
        return -1.0
    return ((end / begin) ** (1 / years) - 1) * 100


def daily_returns(series: list[float]) -> list[float]:
    out = []
    for i in range(1, len(series)):
        prev = series[i - 1]
        if prev != 0:
            out.append((series[i] - prev) / prev)
    return out


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def std(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def volatility_pct(returns: list[float]) -> float:
    return std(returns) * math.sqrt(252) * 100


def sharpe(returns: list[float]) -> float:
    s = std(returns)
    if s == 0:
        return 0.0
    return (mean(returns) - RISK_FREE_DAILY) / s * math.sqrt(252)


def sortino(returns: list[float]) -> float:
    downside = [r for r in returns if r < 0]
    ds = std(downside) if len(downside) >= 2 else 0.0
    if ds == 0:
        return 0.0
    return (mean(returns) - RISK_FREE_DAILY) / ds * math.sqrt(252)


def max_drawdown_pct(series: list[float]) -> float:
    peak = series[0] if series else 0.0
    worst = 0.0
    for v in series:
        peak = max(peak, v)
        if peak > 0:
            worst = min(worst, (v - peak) / peak)
    return worst * 100


def herfindahl_score(weights: list[float]) -> float:
    """Normalized diversification score: 1 = perfectly spread, 0 = single asset."""
    total = sum(weights)
    if total <= 0:
        return 0.0
    hhi = sum((w / total) ** 2 for w in weights)
    n = len(weights)
    if n <= 1:
        return 0.0
    # normalize HHI to [0,1] then invert
    hhi_norm = (hhi - 1 / n) / (1 - 1 / n)
    return max(0.0, min(1.0, 1 - hhi_norm))


def interpret(score: float) -> str:
    if score >= 0.75:
        return "well diversified"
    if score >= 0.45:
        return "moderately diversified"
    return "concentrated"
