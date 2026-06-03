from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.messaging.contracts.events import Event

    from template_app.runtime.messaging.registry import RuntimeHandlerRegistry


@dataclass(slots=True)
class RuntimeEventBus:
    """In-memory runtime event bus."""

    registry: RuntimeHandlerRegistry

    async def publish(self, event: Event) -> None:

        handlers = self.registry.get_event_handlers(type(event))

        for handler in handlers:
            await handler(event)
