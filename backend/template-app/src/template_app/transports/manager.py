"""Transport runtime manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.transports.contracts import Transport


@dataclass(slots=True)
class TransportManager:
    """
    Runtime transport registry/orchestrator.

    Responsibilities:
        - transport ownership
        - lifecycle orchestration
        - transport isolation
    """

    _transports: list[Transport] = field(default_factory=list)

    ###############
    # transport API
    ###############

    def install(self, transport: Transport) -> None:
        """Install runtime transport."""
        self._transports.append(transport)

    ################
    # public queries
    ################

    @property
    def transports(self) -> tuple[Transport, ...]:
        """Return immutable list of installed transports."""
        return tuple(self._transports)

    def get(self, transport_type: type[Transport]) -> Transport | None:
        """Return installed transport by type."""
        return next(
            (
                transport
                for transport in self._transports
                if isinstance(transport, transport_type)
            ),
            None,
        )

    ################
    # lifecycle API
    ################

    async def startup(self) -> None:
        """Start installed transports."""
        for transport in self._transports:
            await transport.startup()

    async def shutdown(self) -> None:
        """Shutdown installed transports."""
        for transport in reversed(self._transports):
            await transport.shutdown()
