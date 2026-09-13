"""Portfolio analytics routes: summary, risk metrics, history."""
from fastapi import APIRouter, Query

from ..schemas.portfolio import HistoryResponse, PortfolioSummary, RiskMetrics
from ..services import metrics, store
from .holdings import _summary

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/summary", response_model=PortfolioSummary)
def summary():
    return _summary(store.DEMO_HOLDINGS)


@router.get("/metrics", response_model=RiskMetrics)
def risk_metrics():
    total = store.curve_total_value()
    curve = store.scale_curve_to(total, days=365)
    rets = metrics.daily_returns(curve)
    return RiskMetrics(
        cagr_pct=round(metrics.cagr(curve[0], curve[-1], len(curve)), 2),
        volatility_pct=round(metrics.volatility_pct(rets), 2),
        sharpe_ratio=round(metrics.sharpe(rets), 3),
        sortino_ratio=round(metrics.sortino(rets), 3),
        max_drawdown_pct=round(metrics.max_drawdown_pct(curve), 2),
        risk_free_rate_pct=7.0,
    )


@router.get("/history", response_model=HistoryResponse)
def history(days: int = Query(default=365, ge=30, le=1095)):
    total = store.curve_total_value()
    curve = store.scale_curve_to(total, days=days)
    dd = store.drawdown_series(curve)
    pts = [
        {"day": i, "value": round(v, 2), "drawdown_pct": round(d, 3)}
        for i, (v, d) in enumerate(zip(curve, dd))
    ]
    return HistoryResponse(days=days, points=pts)
