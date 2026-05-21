from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from template_app.bootstrap.lifecycle.hooks import LifecycleHook
from template_app.bootstrap.modules.capabilities import ModuleCapability
from template_app.bootstrap.modules.manifests import ModuleManifest
from template_app.bootstrap.modules.registry import ModuleRegistry

if TYPE_CHECKING:
    from template_app.bootstrap.modules.context import ModuleSetupContext


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

    started: bool = False

    async def startup_hook(self) -> None:
        self.started = True

    async def shutdown_hook(self) -> None:
        self.started = False

    def setup(self, context: ModuleSetupContext) -> None:

        router: APIRouter = APIRouter(tags=["runtime"])

        @router.get("/runtime")
        async def runtime() -> dict[str, str]:
            return {"runtime": "active"}

        context.register_router(router)

        context.register_startup_hook(
            LifecycleHook(
                name="runtime.startup",
                handler=self.startup_hook,
            ),
        )

        context.register_shutdown_hook(
            LifecycleHook(
                name="runtime.shutdown",
                handler=self.shutdown_hook,
            ),
        )


registry: ModuleRegistry = ModuleRegistry()

registry.register(
    ModuleManifest(
        name="health",
        module=HealthModule(),
        capabilities=frozenset({ModuleCapability.ROUTER}),
    )
)

registry.register(
    ModuleManifest(
        name="runtime",
        module=RuntimeModule(),
        capabilities=frozenset({
            ModuleCapability.ROUTER,
            ModuleCapability.LIFECYCLE,
        }),
    )
)

MODULE_REGISTRY: ModuleRegistry = registry
