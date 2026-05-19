from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.messaging.contracts.commands import Command
    from template_app.bootstrap.messaging.runtime.registry import (
        RuntimeHandlerRegistry,
    )


@dataclass(slots=True)
class RuntimeCommandBus:
    """Runtime command bus."""

    registry: RuntimeHandlerRegistry

    async def execute(self, command: Command) -> None:

        handler = self.registry.get_command_handler(type(command))

        await handler(command)
