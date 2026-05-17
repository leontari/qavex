from __future__ import annotations

from template_app.bootstrap.module_context import ModuleSetupContext
from template_app.bootstrap.contracts import ModuleProtocol, DependencyProvider
from template_app.bootstrap.runtime.bootstrap import bootstrap_application
from template_app.bootstrap.contracts.types import DependencyScope


class FakeProvider:
    """Fake dependency provider."""

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> DependencyScope:
        return DependencyScope.SINGLETON

    def provide(self) -> object:
        return object()


class FakeModule:
    """Fake module for protocol validation."""

    def setup(self, context: ModuleSetupContext) -> None:
        provider: DependencyProvider = FakeProvider

        context.register_dependency(provider)


def test_module_protocol_compatible() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    module: ModuleProtocol = FakeModule()

    module.setup(context)

    assert kernel.context.runtime.container.contains("fake") is True
