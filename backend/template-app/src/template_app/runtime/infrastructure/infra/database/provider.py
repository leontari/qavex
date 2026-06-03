"""Provider Example."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Coroutine


@dataclass(slots=True)
class DatabaseProvider:
    """Database infrastructure provider."""

    dsn: str

    started: bool = field(
        default=False,
        init=False,
    )

    @property
    def name(self) -> str:
        return "database"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False
