from __future__ import annotations

from fastapi import APIRouter

from template_app.runtime.lifecycle.hooks import LifecycleHook
from template_app.runtime.module.context import ModuleContext


class FakeModule:
    """Fake testing module."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.stopped = True

    def setup(self, context: ModuleContext) -> None:

        router = APIRouter()

        @router.get("/fake")
        async def fake() -> dict[str, str]:
            return {"status": "ok"}

        context.register_router(router)

        context.register_startup_hook(
            LifecycleHook(
                name="fake.startup",
                handler=self.startup,
            )
        )

        context.register_shutdown_hook(
            LifecycleHook(
                name="fake.shutdown",
                handler=self.shutdown,
            )
        )


def build_fake_module() -> FakeModule:
    """Build fake module."""

    return FakeModule()
