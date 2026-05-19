from __future__ import annotations

from typing import Any, Protocol

from template_app.bootstrap.messaging.contracts.commands import Command
from template_app.bootstrap.messaging.contracts.events import Event
from template_app.bootstrap.messaging.contracts.queries import Query


class EventBusProtocol(Protocol):
    async def publish(self, event: Event) -> None: ...


class CommandBusProtocol(Protocol):
    async def execute(self, command: Command) -> None: ...


class QueryBusProtocol(Protocol):
    async def ask(self, query: Query) -> Any: ...
