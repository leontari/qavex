from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from template_app.bootstrap.registry import ModuleRegistry

if TYPE_CHECKING:
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

        router = APIRouter(tags=["health"])

        @router.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok"}

        app.include_router(router)


class RuntimeModule:
    """Runtime diagnostics module."""

    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        router = APIRouter(tags=["runtime"])

        @router.get("/runtime")
        async def runtime() -> dict[str, str]:
            return {
                "runtime": "active",
            }

        app.include_router(router)


registry = ModuleRegistry()

registry.extend(
    [
        HealthModule(),
        RuntimeModule(),
    ],
)

MODULES: tuple[ModuleProtocol, ...] = registry.modules
