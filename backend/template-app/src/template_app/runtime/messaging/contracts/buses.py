from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from .commands import Command
    from .events import Event
    from .queries import Query


class EventBusProtocol(Protocol):
    async def publish(self, event: Event) -> None: ...


class CommandBusProtocol(Protocol):
    async def execute(self, command: Command) -> None: ...


class QueryBusProtocol(Protocol):
    async def ask(self, query: Query) -> Any: ...
