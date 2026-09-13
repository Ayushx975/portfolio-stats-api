"""FastAPI app entry point."""
from fastapi import FastAPI

from .routers import holdings, portfolio

app = FastAPI(
    title="Portfolio Stats API",
    description="Investment portfolio analytics: returns, risk metrics, diversification.",
    version="1.0.0",
)

app.include_router(holdings.router)
app.include_router(portfolio.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
