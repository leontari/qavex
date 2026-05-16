"""Database provider."""

from __future__ import annotations


class DatabaseProvider:
    """Database infrastructure provider."""

    name = "database"

    def __init__(self) -> None:
        self.started = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False
