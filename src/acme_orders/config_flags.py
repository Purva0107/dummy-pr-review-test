"""Feature flags / runtime toggles."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FeatureFlags:
    enable_tier_discounts: bool = True
    enable_guest_checkout: bool = True
    enable_order_emails: bool = True
    enable_soft_inventory_holds: bool = False
    max_discount_bps: int = 3000
    extras: dict[str, str] = field(default_factory=dict)

    def get(self, key: str, default: str | None = None) -> str | None:
        return self.extras.get(key, default)


_FLAGS = FeatureFlags()


def get_feature_flags() -> FeatureFlags:
    return _FLAGS


def reset_feature_flags() -> None:
    global _FLAGS
    _FLAGS = FeatureFlags()
