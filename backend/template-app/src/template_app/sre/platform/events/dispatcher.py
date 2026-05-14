"""
Runtime event dispatcher.

Responsible for orchestrating runtime event delivery.
"""

from __future__ import annotations

from template_app.platform.events.bus import RuntimeEventBus
from template_app.platform.events.models import RuntimeEvent


class EventDispatcher:
    """
    Runtime event dispatcher facade.
    """

    def __init__(
        self,
        bus: RuntimeEventBus,
    ) -> None:
        self.bus = bus

    async def dispatch(
        self,
        event: RuntimeEvent,
    ) -> None:
        """
        Dispatch runtime event.
        """
        await self.bus.emit(event)
