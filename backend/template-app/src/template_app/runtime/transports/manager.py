"""Transport runtime manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

from template_app.runtime.transports.contracts import Transport

T = TypeVar("T", bound=Transport)


@dataclass(slots=True)
class TransportManager:
    """
    Typed registry/orchestrator for runtime transports.

    Responsibilities:
        - transport ownership
        - lifecycle orchestration
        - transport isolation
    """

    _transports: dict[type[Transport], Transport] = field(default_factory=dict)

    ###############
    # transport API
    ###############

    def install(self, transport: Transport) -> None:
        """Install runtime transport."""
        self._transports[type(transport)] = transport

    ################
    # public queries
    ################

    @property
    def transports(self) -> tuple[Transport, ...]:
        """Return immutable list of installed transports."""
        return tuple(self._transports.values())

    def get(self, transport_type: type[T]) -> T | None:
        """Return installed transport by type."""
        return self._transports.get(transport_type)

    ################
    # lifecycle API
    ################

    async def startup(self) -> None:
        """Start installed transports."""
        for transport in self._transports.values():
            await transport.startup()

    async def shutdown(self) -> None:
        """Shutdown installed transports."""
        for transport in reversed(self._transports.values()):
            await transport.shutdown()
