"""Transport runtime manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

from template_app.runtime.transports.contracts import Transport

T = TypeVar("T", bound=Transport)


@dataclass(slots=True)
class TransportManager:
    """
    Transport runtime manager.

    Responsibilities:
        - transport ownership
        - startup coordination
        - shutdown coordination
    """

    _transports: list[Transport] = field(
        default_factory=list,
    )

    def install(self, transport: Transport) -> None:
        """Append runtime transport."""
        if transport in self._transports:
            return

        self._transports.append(transport)

    @property
    def transports(self) -> tuple[Transport, ...]:
        """Return immutable list of installed transports."""
        return tuple(self._transports)

    def get(self, transport_type: type[T]) -> T | None:
        """Return installed transport by type."""
        for transport in self._transports:
            if isinstance(transport, transport_type):
                return transport
        return None

    async def startup(self) -> None:
        """Start installed transports."""
        for transport in self._transports:
            await transport.startup()

    async def shutdown(self) -> None:
        """Shutdown installed transports."""
        for transport in reversed(self._transports):
            await transport.shutdown()
