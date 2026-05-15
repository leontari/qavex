from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from fastapi import FastAPI

    from template_app.bootstrap.container import Container
    from template_app.bootstrap.protocols import ModuleProtocol


class HealthModule:
    """Platform health module."""

    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        @app.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok"}


MODULES: Sequence[ModuleProtocol] = [
    HealthModule(),
]
