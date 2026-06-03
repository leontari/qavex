from __future__ import annotations

from template_app.runtime.messaging.contracts.commands import (
    Command,
)
from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)


class FakeCommand(Command):
    pass


async def handler(_: Command) -> None:
    pass


def test_registry_registers_command_handler() -> None:

    registry = RuntimeHandlerRegistry()

    registry.register_command_handler(
        FakeCommand,
        handler,
    )

    resolved = registry.get_command_handler(
        FakeCommand,
    )

    assert resolved is handler
