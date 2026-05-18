from __future__ import annotations

import pytest

from template_app.bootstrap.events.dispatcher import EventDispatcher
from template_app.bootstrap.events.event import Event
from template_app.bootstrap.events.registry import EventRegistry


@pytest.mark.asyncio
async def test_dispatcher_executes_handlers() -> None:

    executed = False

    async def handler(event: Event) -> None:
        nonlocal executed
        executed = True

    registry = EventRegistry()

    registry.subscribe("test.event", handler)

    dispatcher = EventDispatcher(registry=registry)

    await dispatcher.dispatch(Event(name="test.event"))

    assert executed is True
