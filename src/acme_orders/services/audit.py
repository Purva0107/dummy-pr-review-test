"""Audit trail helpers for order lifecycle events."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from acme_orders.utils.timeutil import to_iso, utc_now

logger = logging.getLogger(__name__)


@dataclass
class AuditEvent:
    action: str
    entity_type: str
    entity_id: str
    actor: str
    at: datetime = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        payload = asdict(self)
        payload["at"] = to_iso(self.at)
        return json.dumps(payload, sort_keys=True)


class AuditLogger:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: str | int,
        actor: str = "system",
        **metadata: Any,
    ) -> AuditEvent:
        event = AuditEvent(
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id),
            actor=actor,
            metadata=metadata,
        )
        self._events.append(event)
        logger.info("audit %s", event.to_json())
        return event

    def for_entity(self, entity_type: str, entity_id: str | int) -> list[AuditEvent]:
        eid = str(entity_id)
        return [e for e in self._events if e.entity_type == entity_type and e.entity_id == eid]

    def clear(self) -> None:
        self._events.clear()


_AUDIT = AuditLogger()


def get_audit_logger() -> AuditLogger:
    return _AUDIT
