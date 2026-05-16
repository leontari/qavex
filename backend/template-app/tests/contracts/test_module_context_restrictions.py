from __future__ import annotations

from template_app.bootstrap.module_context import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_module_context_hides_runtime() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    assert not hasattr(context, "runtime")
    assert not hasattr(context, "container")
    assert not hasattr(context, "lifecycle_registry")
