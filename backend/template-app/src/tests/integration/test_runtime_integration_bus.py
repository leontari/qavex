from __future__ import annotations

import pytest

from template_app.bootstrap.integration.bus import (
    RuntimeIntegrationBus,
)
from template_app.bootstrap.integration.models import (
    IntegrationEvent,
)
from template_app.bootstrap.integration.registry import (
    IntegrationHandlerRegistry,
)


class UserCreatedEvent(IntegrationEvent):
    pass


@pytest.mark.asyncio
async def test_runtime_integration_bus_executes_handlers() -> None:

    registry = IntegrationHandlerRegistry()

    executed = False

    async def handler(_: IntegrationEvent) -> None:
        nonlocal executed
        executed = True

    registry.subscribe(
        UserCreatedEvent,
        handler,
    )

    bus = RuntimeIntegrationBus(
        registry=registry,
    )

    await bus.publish(
        UserCreatedEvent(name="user_created"),
    )

    assert executed is True
