from __future__ import annotations

from fastapi import APIRouter, FastAPI

from template_app.bootstrap.contracts import DependencyProvider, \
    DependencyScope
from tests.factories.kernel import build_testing_kernel
from template_app.bootstrap.modules.context import ModuleSetupContext
from template_app.bootstrap.contracts.modules import ModuleProtocol


class FakeProvider:

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> DependencyScope:
        return DependencyScope.SINGLETON

    def provide(self) -> str:
        return "value"


class FakeModule:
    """Fake module for protocol validation."""

    def setup(self, context: ModuleSetupContext) -> None:

        router = APIRouter()

        @router.get("/fake")
        async def fake() -> dict[str, str]:
            return {"ok": "true"}

        context.register_router(router)

        provider: DependencyProvider = FakeProvider()

        context.register_dependency(provider)


def test_module_protocol_compatible() -> None:
    kernel = build_testing_kernel()

    module: ModuleProtocol = FakeModule()

    context = ModuleSetupContext(_kernel=kernel) # TODO: check protect necessity

    module.setup(context)

    assert kernel.context.runtime.container.contains("fake") is True
