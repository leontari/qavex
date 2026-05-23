from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.transports.contracts import Transport


@dataclass(slots=True)
class TransportManager:
    _transports: dict[str, Transport] = field(default_factory=dict)

    def register(self, transport: Transport) -> None:
        self._transports[transport.name] = transport

    def list(self) -> tuple[Transport, ...]:
        return tuple(self._transports.values())

    async def startup(self) -> None:
        for t in self._transports.values():
            await t.startup()

    async def shutdown(self) -> None:
        for t in self._transports.values():
            await t.shutdown()
