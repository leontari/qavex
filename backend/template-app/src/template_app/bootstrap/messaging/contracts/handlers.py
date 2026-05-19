from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from template_app.bootstrap.messaging.contracts.commands import Command
    from template_app.bootstrap.messaging.contracts.events import Event
    from template_app.bootstrap.messaging.contracts.queries import Query


class EventHandler(Protocol):
    async def __call__(self, event: Event) -> None: ...


class CommandHandler(Protocol):
    async def __call__(self, command: Command) -> None: ...


class QueryHandler(Protocol):
    async def __call__(self, query: Query) -> Any: ...
