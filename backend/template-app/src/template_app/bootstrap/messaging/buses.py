from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.bootstrap.messaging.commands import Command
    from template_app.bootstrap.messaging.queries import Query
    from template_app.bootstrap.messaging.registry import (
        MessageHandlerRegistry,
    )


@dataclass(slots=True)
class CommandBus:
    """Command execution bus."""

    registry: MessageHandlerRegistry

    async def dispatch(self, command: Command) -> Any:
        handler = self.registry.get_command_handler(type(command))
        return await handler.handle(command)


@dataclass(slots=True)
class QueryBus:
    """Query execution bus."""

    registry: MessageHandlerRegistry

    async def execute(self, query: Query) -> Any:
        handler = self.registry.get_query_handler(type(query))
        return await handler.handle(query)
