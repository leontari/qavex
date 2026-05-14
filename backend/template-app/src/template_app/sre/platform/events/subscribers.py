from __future__ import annotations

from typing import Protocol

from template_app.platform.events.models import RuntimeEvent


class EventSubscriber(Protocol):
    """Runtime event subscriber contract."""

    async def handle(
        self,
        event: RuntimeEvent,
    ) -> None:
        """Handle runtime event."""
