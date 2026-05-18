from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.events.event import Event
from template_app.bootstrap.events.registry import EventRegistry


@dataclass(slots=True)
class EventDispatcher:
    """Runtime event dispatcher."""

    registry: EventRegistry

    async def dispatch(self, event: Event) -> None:

        handlers = self.registry.get_handlers(event.name)

        for handler in handlers:
            await handler(event)
