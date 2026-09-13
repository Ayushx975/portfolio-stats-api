"""Seeded deterministic demo data — no external market API needed."""
from __future__ import annotations

import math
import random

from ..schemas.portfolio import Holding

DEMO_HOLDINGS = [
    Holding(symbol="NIFTYBEES", units=50, avg_cost=210.0, last_price=285.0),
    Holding(symbol="GOLDBEES", units=100, avg_cost=42.0, last_price=58.0),
    Holding(symbol="LIQUIDBEES", units=200, avg_cost=1000.0, last_price=1012.0),
    Holding(symbol="ITBEES", units=30, avg_cost=38.0, last_price=44.5),
]


def equity_curve(days: int = 365, seed: int = 11) -> list[float]:
    """Deterministic pseudo-random walk for the demo portfolio history."""
    rng = random.Random(seed)
    value = 120000.0
    out = [value]
    for _ in range(days - 1):
        drift = 0.0004
        shock = rng.gauss(0.0, 0.008)
        value *= 1 + drift + shock
        out.append(max(value, 1000.0))
    return out


def drawdown_series(series: list[float]) -> list[float]:
    peak = series[0]
    out = []
    for v in series:
        peak = max(peak, v)
        out.append((v - peak) / peak * 100 if peak > 0 else 0.0)
    return out


def curve_total_value() -> float:
    return sum(h.units * h.last_price for h in DEMO_HOLDINGS)


def scale_curve_to(holdings_value: float, days: int = 365) -> list[float]:
    base = equity_curve(days)
    end = base[-1]
    k = holdings_value / end
    return [v * k for v in base]
