from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from template_app.bootstrap.registry import ModuleRegistry
from template_app.bootstrap.runtime.hooks import LifecycleHook

if TYPE_CHECKING:
    from template_app.bootstrap.module_context import ModuleSetupContext
    from template_app.bootstrap.protocols import ModuleProtocol


class HealthModule:
    """Application health module."""

    def setup(self, context: ModuleSetupContext) -> None:

        router: APIRouter = APIRouter(tags=["health"])

        @router.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok"}

        context.register_router(router)


class RuntimeModule:
    """Runtime diagnostics module."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    async def startup_hook(self) -> None:
        self.started = True

    async def shutdown_hook(self) -> None:
        self.stopped = True

    def setup(self, context: ModuleSetupContext) -> None:

        router: APIRouter = APIRouter(tags=["runtime"])

        @router.get("/runtime")
        async def runtime() -> dict[str, str]:
            return {"runtime": "active"}

        context.register_router(router)

        context.register_startup_hook(
            LifecycleHook(
                name="runtime_startup",
                handler=self.startup_hook,
            ),
        )

        context.register_shutdown_hook(
            LifecycleHook(
                name="runtime_shutdown",
                handler=self.shutdown_hook,
            ),
        )


registry: ModuleRegistry = ModuleRegistry()

registry.extend(
    [
        HealthModule(),
        RuntimeModule(),
    ],
)

MODULES: tuple[ModuleProtocol, ...] = registry.modules
