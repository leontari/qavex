from __future__ import annotations

from fastapi import APIRouter

from template_app.runtime.lifecycle.hooks import (
    LifecycleHook,
)
from template_app.runtime.modules.context import (
    ModuleContext,
)


class FakeRuntimeModule:

    started: bool = False

    async def startup_hook(self) -> None:
        self.started = True

    async def shutdown_hook(self) -> None:
        self.started = False

    def setup(
        self,
        context: ModuleContext,
    ) -> None:

        router = APIRouter()

        @router.get("/runtime")
        async def runtime() -> dict[str, str]:
            return {"status": "ok"}

        context.register_router(router)

        context.register_startup_hook(
            LifecycleHook(
                name="fake_runtime.startup",
                handler=self.startup_hook,
            ),
        )

        context.register_shutdown_hook(
            LifecycleHook(
                name="fake_runtime.shutdown",
                handler=self.shutdown_hook,
            ),
        )
