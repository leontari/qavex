from __future__ import annotations

from typing import Protocol

from template_app.bootstrap.events.event import Event


class EventHandler(Protocol):
    async def __call__(self, event: Event) -> None: ...


class EventBusProtocol(Protocol):
    async def publish(self, event: Event) -> None: ...

    def subscribe(self, event_name: str, handler: EventHandler) -> None: ...
