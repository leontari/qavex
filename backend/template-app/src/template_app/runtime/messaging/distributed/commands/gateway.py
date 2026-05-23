from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from template_app.runtime.messaging.contracts.commands import Command


class DistributedCommandGateway(Protocol):
    async def send(self, command: Command) -> None: ...
