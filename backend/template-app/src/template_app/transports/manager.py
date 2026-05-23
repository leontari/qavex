from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.transports.contracts import Transport


@dataclass(slots=True)
class TransportManager:
    _transports: list[Transport] = field(default_factory=list)

    def install(self, transport: Transport) -> None:
        self._transports.append(transport)

    async def startup(self) -> None:

        for transport in self._transports:
            await transport.startup()

    async def shutdown(self) -> None:

        for transport in reversed(self._transports):
            await transport.shutdown()
