from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.runtime.transports.gating import TransportGate


@dataclass(slots=True)
class FastAPITransport:
    """
    HTTP transport runtime.

    Responsibilities:
        - ASGI runtime ownership
        - HTTP lifecycle
        - readiness gating

    """

    app: FastAPI

    gate: TransportGate | None = None

    name: str = "http"

    async def startup(self) -> None:
        """Start HTTP transport."""
        if self.gate and not self.gate.allow_start():
            return

    async def shutdown(self) -> None:
        """Shutdown HTTP transport."""
