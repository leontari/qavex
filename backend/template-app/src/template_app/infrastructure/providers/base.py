"""Provider Protocol."""

from __future__ import annotations

from typing import Protocol


class InfrastructureProvider(Protocol):
    """Infrastructure provider contract."""

    name: str

    async def startup(self) -> None:
        """Start provider."""

    async def shutdown(self) -> None:
        """Shutdown provider."""
