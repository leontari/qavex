from __future__ import annotations

import pytest

from template_app.bootstrap.dispatching.commands.dispatcher import (
    CommandDispatcher,
)
from template_app.bootstrap.dispatching.commands.models import (
    Command,
)
from template_app.bootstrap.dispatching.registry import (
    MessageHandlerRegistry,
)


class CreateUserCommand(Command):
    pass


@pytest.mark.asyncio
async def test_command_dispatcher_executes_handler() -> None:

    registry = MessageHandlerRegistry()

    executed = False

    async def handler(_: Command) -> None:
        nonlocal executed
        executed = True

    registry.register_command(
        CreateUserCommand,
        handler,
    )

    dispatcher = CommandDispatcher(
        registry=registry,
    )

    await dispatcher.execute(
        CreateUserCommand(),
    )

    assert executed is True
