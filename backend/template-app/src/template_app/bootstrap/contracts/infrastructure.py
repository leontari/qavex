"""Infrastructure provider contract."""

from __future__ import annotations

from typing import Protocol


class InfrastructureProvider(Protocol):
    """Infrastructure runtime provider contract."""

    @property
    def name(self) -> str:
        """Provider name."""

    async def startup(self) -> None:
        """Startup infrastructure."""

    async def shutdown(self) -> None:
        """Shutdown infrastructure."""
