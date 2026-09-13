"""Pydantic models for requests and responses."""
from pydantic import BaseModel, Field


class Holding(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    units: float = Field(..., gt=0)
    avg_cost: float = Field(..., gt=0)
    last_price: float = Field(..., gt=0)


class HoldingsPayload(BaseModel):
    holdings: list[Holding] = Field(..., min_length=1)


class HoldingOut(Holding):
    market_value: float
    invested_value: float
    pnl: float
    pnl_pct: float
    weight: float


class Diversification(BaseModel):
    score: float
    interpretation: str


class PortfolioSummary(BaseModel):
    total_value: float
    total_cost: float
    pnl: float
    pnl_pct: float
    holdings: list[HoldingOut]
    diversification: Diversification


class RiskMetrics(BaseModel):
    cagr_pct: float
    volatility_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown_pct: float
    risk_free_rate_pct: float


class CurvePoint(BaseModel):
    day: int
    value: float
    drawdown_pct: float


class HistoryResponse(BaseModel):
    days: int
    points: list[CurvePoint]
