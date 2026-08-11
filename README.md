# Acme Orders API

Internal order management service for **Acme Retail**.

## Stack

- Python 3.11+
- FastAPI
- SQLite (local/dev) via SQLAlchemy
- Pytest

## Quick start

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
export PYTHONPATH=src   # Windows PowerShell: $env:PYTHONPATH="src"
pytest -q
uvicorn acme_orders.main:app --reload --app-dir src
```

Health: `GET http://127.0.0.1:8000/health`

## Layout

```
src/acme_orders/
  api/         HTTP routers and dependencies
  auth/        API key authentication
  db/          SQLAlchemy session + repositories
  models/      Domain / API schemas
  services/    Business logic (orders, pricing, inventory)
  utils/       Money, validation, time helpers
```

## Auth

Send header `X-API-Key: <ACME_API_KEY>` (default in `.env.example`).

## License

Internal use only — Acme Retail engineering.
