from __future__ import annotations

from template_app.bootstrap.modules import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import  bootstrap_application
from tests.factories.module_context import build_module_context


def test_module_context_created() -> None:
    kernel = bootstrap_application()

    assert kernel.context.app is not None
