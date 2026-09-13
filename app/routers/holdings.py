"""Holdings routes: view demo holdings, analyze custom ones."""
from fastapi import APIRouter

from ..schemas.portfolio import HoldingsPayload, HoldingOut, PortfolioSummary
from ..services import metrics, store

router = APIRouter(prefix="/holdings", tags=["holdings"])


def _summary(holdings) -> PortfolioSummary:
    invested = [h.units * h.avg_cost for h in holdings]
    market = [h.units * h.last_price for h in holdings]
    total_inv, total_mkt = sum(invested), sum(market)
    pnl = total_mkt - total_inv
    outs = []
    for h, inv, mkt in zip(holdings, invested, market):
        p = mkt - inv
        outs.append(HoldingOut(
            **h.model_dump(),
            market_value=round(mkt, 2),
            invested_value=round(inv, 2),
            pnl=round(p, 2),
            pnl_pct=round(p / inv * 100, 2) if inv else 0.0,
            weight=round(mkt / total_mkt * 100, 2) if total_mkt else 0.0,
        ))
    score = metrics.herfindahl_score(market)
    return PortfolioSummary(
        total_value=round(total_mkt, 2),
        total_cost=round(total_inv, 2),
        pnl=round(pnl, 2),
        pnl_pct=round(pnl / total_inv * 100, 2) if total_inv else 0.0,
        holdings=outs,
        diversification={"score": round(score, 3), "interpretation": metrics.interpret(score)},
    )


@router.get("", response_model=list[HoldingOut])
def current_holdings():
    return _summary(store.DEMO_HOLDINGS).holdings


@router.post("/analyze", response_model=PortfolioSummary)
def analyze(payload: HoldingsPayload):
    return _summary(payload.holdings)
