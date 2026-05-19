from __future__ import annotations

import pytest

from template_app.bootstrap.messaging.contracts.events import (
    Event,
)
from template_app.bootstrap.messaging.runtime.event_bus import (
    RuntimeEventBus,
)
from template_app.bootstrap.messaging.runtime.registry import (
    RuntimeHandlerRegistry,
)


class UserCreatedEvent(Event):
    pass


@pytest.mark.asyncio
async def test_runtime_event_bus_executes_handlers() -> None:

    registry = RuntimeHandlerRegistry()

    executed = False

    async def handler(_: Event) -> None:
        nonlocal executed
        executed = True

    registry.register_event_handler(
        UserCreatedEvent,
        handler,
    )

    bus = RuntimeEventBus(
        registry=registry,
    )

    await bus.publish(
        UserCreatedEvent(),
    )

    assert executed is True
