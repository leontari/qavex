from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI


@dataclass(slots=True)
class FastAPITransport:
    app: FastAPI

    async def startup(self) -> None:
        """Start HTTP transport."""

    async def shutdown(self) -> None:
        """Shutdown HTTP transport."""
