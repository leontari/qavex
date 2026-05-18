from __future__ import annotations

from template_app.bootstrap.modules import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import  bootstrap_application


def test_module_context_created() -> None:
    kernel = bootstrap_application()

    context = ModuleSetupContext(_kernel=kernel)

    assert context.app is not None
