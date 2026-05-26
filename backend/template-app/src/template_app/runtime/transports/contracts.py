"""Transport contracts."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Transport(Protocol):
    """Runtime transport contract."""

    name: str

    async def startup(self) -> None:
        """Start transport runtime."""

    async def shutdown(self) -> None:
        """Shutdown transport runtime."""
