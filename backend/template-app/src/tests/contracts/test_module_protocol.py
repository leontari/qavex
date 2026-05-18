from __future__ import annotations

from fastapi import APIRouter, FastAPI
from tests.factories.runtime import build_runtime_state
from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.kernel.context import ApplicationContext
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from template_app.bootstrap.modules.context import ModuleSetupContext
from template_app.bootstrap.contracts.modules import ModuleProtocol
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.bootstrap.lifecycle.registry import (
    LifecycleRegistry,
)
from template_app.bootstrap.lifecycle.manager import (
    LifecycleManager,
)
from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)


class FakeModule:
    """Fake module for protocol validation."""

    def setup(self, context: ModuleSetupContext) -> None:
        router = APIRouter()

        @router.get("/fake")
        async def fake() -> dict[str, str]:
            return {"ok": "true"}

        context.register_router(router)


def test_module_protocol_compatible() -> None:
    runtime = build_runtime_state()

    context = ApplicationContext(runtime=runtime)

    app = FastAPI()

    context.app = app

    kernel = RuntimeKernel(context=context)

    module_context = ModuleSetupContext(kernel)

    module: ModuleProtocol = FakeModule()

    module.setup(module_context)

    assert any(
        route.path == "/fake"
        for route in kernel.context.app.routes
    )
