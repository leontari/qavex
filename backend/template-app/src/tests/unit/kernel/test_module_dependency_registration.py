from __future__ import annotations

from template_app.bootstrap.modules import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import bootstrap_application
from template_app.infrastructure.cache import CacheProvider


def test_module_can_register_dependency() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    provider = CacheProvider(url="redis://localhost",)

    context.register_dependency(provider)

    resolved = (
        kernel.context
        .runtime
        .container
        .resolve("cache")
    )

    assert resolved is provider
