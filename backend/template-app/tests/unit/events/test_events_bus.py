from __future__ import annotations

import pytest

from template_app.bootstrap.events.bus import EventBus
from template_app.bootstrap.events.dispatcher import EventDispatcher
from template_app.bootstrap.events.event import Event
from template_app.bootstrap.events.registry import EventRegistry


@pytest.mark.asyncio
async def test_event_bus_publish() -> None:

    called = False

    async def handler(event: Event) -> None:
        nonlocal called
        called = True

    registry = EventRegistry()

    dispatcher = EventDispatcher(registry=registry)

    bus = EventBus(registry=registry, dispatcher=dispatcher)

    bus.subscribe("runtime.test", handler)

    await bus.publish(Event(name="runtime.test"))

    assert called is True
