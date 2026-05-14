from __future__ import annotations

from enum import StrEnum


class RuntimeEventType(StrEnum):
    """Runtime platform event types."""

    HEALTH_CHANGED = "health_changed"

    SERVICE_DEGRADED = "service_degraded"

    SERVICE_RECOVERED = "service_recovered"

    READINESS_LOST = "readiness_lost"

    READINESS_RESTORED = "readiness_restored"

    CIRCUIT_OPENED = "circuit_opened"

    CIRCUIT_CLOSED = "circuit_closed"

    CACHE_DISABLED = "cache_disabled"

    CACHE_ENABLED = "cache_enabled"
