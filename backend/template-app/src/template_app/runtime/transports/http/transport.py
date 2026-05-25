from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.runtime.transports.gating import TransportGate


@dataclass(slots=True)
class FastAPITransport:
    name: str = "http"
    app: FastAPI | None = None

    gate: TransportGate | None = None

    async def startup(self) -> None:
        """Start HTTP transport."""
        if self.gate and not self.gate.allow_start():
            return

    async def shutdown(self) -> None:
        """Shutdown HTTP transport."""
        return
