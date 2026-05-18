from __future__ import annotations

from template_app.bootstrap.modules import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_module_context_has_restricted_api() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    assert hasattr(context, "register_router")
    assert hasattr(context, "register_dependency")
    assert hasattr(context, "register_startup_hook")
    assert not hasattr(context, "runtime")
