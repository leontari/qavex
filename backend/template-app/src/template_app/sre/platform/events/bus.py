from __future__ import annotations

import asyncio
from collections import defaultdict

from template_app.platform.events.models import RuntimeEvent
from template_app.platform.events.subscribers import EventSubscriber


class RuntimeEventBus:
    """
    Async runtime event bus.

    The event bus is the central nervous system of the runtime platform.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventSubscriber]] = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        subscriber: EventSubscriber,
    ) -> None:
        """Register event subscriber."""
        self._subscribers[event_type].append(subscriber)

    async def emit(
        self,
        event: RuntimeEvent,
    ) -> None:
        """Emit runtime event."""
        subscribers = self._subscribers.get(
            event.type,
            [],
        )

        await asyncio.gather(
            *[subscriber.handle(event) for subscriber in subscribers],
            return_exceptions=True,
        )
