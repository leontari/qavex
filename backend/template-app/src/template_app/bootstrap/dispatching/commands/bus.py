from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.commands.models import Command
    from template_app.bootstrap.dispatching.registry import (
        MessageHandlerRegistry,
    )


@dataclass(slots=True)
class InMemoryCommandBus:
    registry: MessageHandlerRegistry

    async def execute(self, command: Command) -> None:

        handler = self.registry._commands[type(command)]

        await handler(command)
