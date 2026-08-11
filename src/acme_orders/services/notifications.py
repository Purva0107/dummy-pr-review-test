"""Notification stubs (email/webhook fans-out in production)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class NotificationRecord:
    channel: str
    recipient: str
    template: str
    payload: dict


@dataclass
class NotificationBus:
    sent: list[NotificationRecord] = field(default_factory=list)

    def send(
        self,
        *,
        channel: str,
        recipient: str,
        template: str,
        payload: dict,
    ) -> NotificationRecord:
        record = NotificationRecord(
            channel=channel,
            recipient=recipient,
            template=template,
            payload=payload,
        )
        self.sent.append(record)
        logger.info(
            "notification queued channel=%s recipient=%s template=%s",
            channel,
            recipient,
            template,
        )
        return record


_BUS = NotificationBus()


def get_notification_bus() -> NotificationBus:
    return _BUS


def reset_notification_bus() -> None:
    _BUS.sent.clear()
