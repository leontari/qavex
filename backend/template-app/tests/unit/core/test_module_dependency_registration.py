from __future__ import annotations

from template_app.bootstrap.module_context import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_module_can_register_dependency() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    dependency = object()

    context.register_dependency("test", dependency)

    resolved = (
        kernel.context
        .runtime
        .container
        .resolve("test")
    )

    assert resolved is dependency
