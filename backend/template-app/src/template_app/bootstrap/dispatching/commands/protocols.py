from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.commands.models import Command


class CommandHandler(Protocol):
    async def __call__(self, command: Command) -> None: ...
