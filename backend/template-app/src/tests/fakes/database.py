from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FakeDatabaseProvider:
    """
    Fake database provider.
    """

    rows: list[Any] = field(default_factory=list)

    started: bool = False

    @property
    def name(self) -> str:
        return "database"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False

    async def insert(
        self,
        row: Any,
    ) -> None:

        self.rows.append(row)

    async def fetch_all(self) -> list[Any]:

        return self.rows
