from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.events.dispatcher import EventDispatcher
from template_app.bootstrap.events.event import Event
from template_app.bootstrap.events.protocols import (
    EventBusProtocol,
    EventHandler,
)
from template_app.bootstrap.events.registry import EventRegistry


@dataclass(slots=True)
class EventBus(EventBusProtocol):
    """Runtime event bus."""

    registry: EventRegistry
    dispatcher: EventDispatcher

    async def publish(self, event: Event) -> None:
        await self.dispatcher.dispatch(event)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self.registry.subscribe(event_name, handler)
