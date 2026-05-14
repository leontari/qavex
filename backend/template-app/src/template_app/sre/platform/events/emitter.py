"""
Runtime event emitter utilities.
"""

from __future__ import annotations

from typing import Any

from template_app.platform.events.bus import RuntimeEventBus
from template_app.platform.events.event_types import (
    RuntimeEventType,
)
from template_app.platform.events.models import RuntimeEvent


class RuntimeEventEmitter:
    """
    High-level runtime event emitter.

    Simplifies emitting strongly typed runtime events.
    """

    def __init__(
        self,
        bus: RuntimeEventBus,
    ) -> None:
        self.bus = bus

    async def emit(
        self,
        event_type: RuntimeEventType,
        source: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """
        Emit runtime event.

        Args:
            event_type:
                Runtime event type.

            source:
                Event source identifier.

            payload:
                Optional structured payload.
        """
        event = RuntimeEvent(
            type=event_type,
            source=source,
            payload=payload or {},
        )

        await self.bus.emit(event)
