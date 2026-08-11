"""SQLAlchemy engine/session helpers."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from acme_orders.config import get_settings


class Base(DeclarativeBase):
    pass


def _ensure_sqlite_dir(url: str) -> None:
    if not url.startswith("sqlite:///"):
        return
    # sqlite:///./data/orders.db or sqlite:////absolute
    raw = url.removeprefix("sqlite:///")
    if raw.startswith("/"):
        path = Path(raw)
    else:
        path = Path(raw)
    if path.parent and str(path.parent) not in (".", ""):
        path.parent.mkdir(parents=True, exist_ok=True)


def create_db_engine(url: str | None = None):
    settings = get_settings()
    db_url = url or settings.database_url
    _ensure_sqlite_dir(db_url)
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    engine = create_engine(db_url, future=True, connect_args=connect_args)

    if db_url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def _fk_on(dbapi_connection, _connection_record):  # type: ignore[no-untyped-def]
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


_engine = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_db_engine()
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


def reset_engine() -> None:
    """Test helper — drop cached engine/session factory."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
    get_settings.cache_clear()


def init_db() -> None:
    from acme_orders.db import tables  # noqa: F401

    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
