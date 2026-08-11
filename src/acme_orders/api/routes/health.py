"""Health and readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from acme_orders import __version__
from acme_orders.api.deps import db_dep, settings_dep
from acme_orders.config import Settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: Settings = Depends(settings_dep)) -> dict:
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": __version__,
        "env": settings.env,
    }


@router.get("/ready")
def ready(session: Session = Depends(db_dep)) -> dict:
    session.execute(text("SELECT 1"))
    return {"status": "ready"}
