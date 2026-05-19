from __future__ import annotations

import pytest

from template_app.bootstrap.messaging.buses import CommandBus
from template_app.bootstrap.messaging.commands import Command
from template_app.bootstrap.messaging.registry import (
    MessageHandlerRegistry,
)


class CreateUser(Command):
    pass


class CreateUserHandler:

    async def handle(self, command: CreateUser) -> str:
        return "created"


@pytest.mark.asyncio
async def test_command_bus_dispatches_command() -> None:
    registry = MessageHandlerRegistry()

    registry.register_command_handler(
        CreateUser,
        CreateUserHandler(),
    )

    bus = CommandBus(registry=registry)

    result = await bus.dispatch(CreateUser())

    assert result == "created"
