from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.commands.models import Command


class CommandHandler(Protocol):
    """Command handler contract."""

    async def handle(self, command: Command) -> Any:
        """Handle command."""
