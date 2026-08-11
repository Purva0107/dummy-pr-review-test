"""Seed local catalog data."""

from __future__ import annotations

import os
import sys

# Allow running as `python scripts/seed_db.py` from repo root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from acme_orders.db.repository import ProductRepository
from acme_orders.db.session import get_session_factory, init_db


CATALOG = [
    ("SKU-TEE-001", "Acme Classic Tee", 2499, 100),
    ("SKU-MUG-002", "Acme Ceramic Mug", 1499, 250),
    ("SKU-HAT-003", "Acme Cap", 1999, 80),
    ("SKU-BAG-004", "Acme Tote", 2999, 60),
    ("SKU-STK-005", "Acme Sticker Pack", 499, 1000),
]


def main() -> None:
    init_db()
    session = get_session_factory()()
    try:
        repo = ProductRepository(session)
        for sku, name, price, stock in CATALOG:
            repo.upsert(
                sku=sku,
                name=name,
                unit_price_cents=price,
                stock_qty=stock,
                active=True,
            )
        session.commit()
        print(f"Seeded {len(CATALOG)} products")
    finally:
        session.close()


if __name__ == "__main__":
    main()
