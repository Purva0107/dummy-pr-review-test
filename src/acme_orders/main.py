"""FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from acme_orders.api.middleware import RequestContextMiddleware
from acme_orders.api.routes import admin, customers, health, orders
from acme_orders.config import get_settings
from acme_orders.db.session import init_db
from acme_orders.logging_setup import configure_logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)
    init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Acme Orders API",
        version="0.1.0",
        description="Internal order management for Acme Retail",
        lifespan=lifespan,
    )
    app.add_middleware(RequestContextMiddleware)
    app.include_router(health.router)
    app.include_router(orders.router)
    app.include_router(customers.router)
    app.include_router(admin.router)

    @app.exception_handler(Exception)
    async def unhandled(_request, exc: Exception):  # type: ignore[no-untyped-def]
        if settings.env == "local":
            return JSONResponse(status_code=500, content={"detail": str(exc)})
        return JSONResponse(status_code=500, content={"detail": "internal error"})

    return app


app = create_app()
