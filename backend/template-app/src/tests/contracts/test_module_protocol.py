from __future__ import annotations

from fastapi import APIRouter

from template_app.bootstrap.contracts import (
    DependencyProvider,
)
from template_app.bootstrap.contracts.modules import (
    ModuleProtocol,
)
from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from tests.factories.module_context import (
    build_module_context,
)


class FakeProvider(DependencyProvider):

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> str:
        return "singleton"

    def provide(self) -> str:
        return "value"


class FakeModule(ModuleProtocol):

    def setup(self, context) -> None:

        router = APIRouter()

        @router.get("/fake")
        async def fake() -> dict[str, str]:
            return {"ok": "true"}

        context.register_router(router)

        context.register_dependency(
            FakeProvider(),
        )


def test_module_protocol_compatible() -> None:

    context = build_module_context(
        frozenset({
            ModuleCapability.ROUTER,
            ModuleCapability.DEPENDENCIES,
        }),
    )

    module: ModuleProtocol = FakeModule()

    module.setup(context)

    assert (
        context.runtime.container.contains("fake")
        is True
    )
