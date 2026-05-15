from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from template_app.bootstrap.registry import ModuleRegistry
from template_app.bootstrap.runtime.hooks import LifecycleHook

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.container import Container
    from template_app.bootstrap.protocols import ModuleProtocol
    from template_app.bootstrap.runtime.registry import LifecycleRegistry


class HealthModule:
    """Platform health module."""

    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:

        router: APIRouter = APIRouter(tags=["health"])

        @router.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok"}

        app.include_router(router)


class RuntimeModule:
    """Runtime diagnostics module."""

    async def startup_hook(self) -> None:
        self.started = True

    async def shutdown_hook(self) -> None:
        self.stooped = True

    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        router: APIRouter = APIRouter(tags=["runtime"])

        @router.get("/runtime")
        async def runtime() -> dict[str, str]:
            return {"runtime": "active"}

        app.include_router(router)

        # TODO: check this
        lifecycle_registry = app.state.lifecycle_registry

        lifecycle_registry.register_startup(
            LifecycleHook(
                name="runtime_startup",
                handler=self.startup_hook,
            ),
        )

        lifecycle_registry.register_shutdown(
            LifecycleHook(
                name="runtime_shutdown",
                handler=self.shutdown_hook,
            )
        )


registry: ModuleRegistry = ModuleRegistry()

registry.extend(
    [
        HealthModule(),
        RuntimeModule(),
    ],
)

MODULES: tuple[ModuleProtocol, ...] = registry.modules
