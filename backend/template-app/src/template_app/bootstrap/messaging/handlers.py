from __future__ import annotations

from typing import Any, Protocol

from template_app.bootstrap.messaging.commands import Command
from template_app.bootstrap.messaging.queries import Query


class CommandHandler(Protocol):
    """Command handler contract."""

    async def handle(self, command: Command) -> Any:
        """Handle command."""


class QueryHandler(Protocol):
    """Query handler contract."""

    async def handle(self, query: Query) -> Any:
        """Handle query."""
