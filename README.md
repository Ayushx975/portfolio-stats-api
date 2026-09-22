# Portfolio Stats API

![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![Tests](https://github.com/Ayushx975/portfolio-stats-api/actions/workflows/ci.yml/badge.svg) ![License MIT](https://img.shields.io/badge/License-MIT-green.svg)

Investment portfolio analytics REST API — returns, risk metrics, and diversification analysis. FastAPI + Pydantic, with clean architecture (routers / services / schemas).

Computes the metrics that actually matter when judging a portfolio:

- **CAGR** — compounded annual growth rate
- **Volatility** — annualized standard deviation of returns
- **Sharpe & Sortino ratios** — risk-adjusted performance
- **Max drawdown** — worst peak-to-trough loss
- **Diversification score** — normalized Herfindahl index over allocations

No market-data API keys needed — a built-in seeded demo dataset is used (deterministic), and custom holdings can be POSTed for full analysis.

## API

| Method | Route | Description |
|---|---|---|
| GET | `/health` | liveness probe |
| GET | `/holdings` | current demo holdings with market values |
| POST | `/holdings/analyze` | analyze custom holdings JSON |
| GET | `/portfolio/summary` | value, cost, P/L, diversification |
| GET | `/portfolio/metrics` | CAGR, vol, Sharpe, Sortino, max drawdown |
| GET | `/portfolio/history?days=365` | equity curve + drawdown series |

Interactive docs at `http://localhost:8000/docs` (Swagger UI auto-generated).

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Sample Analysis

```bash
curl -X POST http://localhost:8000/holdings/analyze \
  -H "Content-Type: application/json" \
  -d '{"holdings": [
        {"symbol": "NIFTYBEES", "units": 50, "avg_cost": 210.0, "last_price": 285.0},
        {"symbol": "GOLDBEES", "units": 100, "avg_cost": 42.0, "last_price": 58.0}
  ]}'
```

```json
{
  "total_value": 20100.0,
  "total_cost": 14700.0,
  "pnl": 5400.0,
  "pnl_pct": 36.7,
  "diversification": {
    "score": 0.62,
    "interpretation": "moderately diversified"
  }
}
```

## Structure

```
app/
├── main.py          # FastAPI app + lifespan
├── routers/         # portfolio, holdings routes
├── services/        # metrics engine, math in pure functions
└── schemas/         # Pydantic request/response models
tests/
└── test_metrics.py  # unit tests for the math (pytest)
```

## Tech

Python 3.11 | FastAPI | Pydantic v2 | pytest | uvicorn

## License

MIT
