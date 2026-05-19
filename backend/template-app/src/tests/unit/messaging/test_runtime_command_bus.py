from __future__ import annotations

import pytest

from template_app.bootstrap.messaging.contracts.commands import (
    Command,
)
from template_app.bootstrap.messaging.runtime.command_bus import (
    RuntimeCommandBus,
)
from template_app.bootstrap.messaging.runtime.registry import (
    RuntimeHandlerRegistry,
)


class CreateUserCommand(Command):
    pass


@pytest.mark.asyncio
async def test_runtime_command_bus_executes_handler() -> None:

    registry = RuntimeHandlerRegistry()

    executed = False

    async def handler(_: Command) -> None:
        nonlocal executed
        executed = True

    registry.register_command_handler(
        CreateUserCommand,
        handler,
    )

    bus = RuntimeCommandBus(
        registry=registry,
    )

    await bus.execute(
        CreateUserCommand(),
    )

    assert executed is True
