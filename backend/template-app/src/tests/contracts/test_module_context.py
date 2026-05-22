from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import  bootstrap_application


def test_module_context_created() -> None:
    kernel = bootstrap_application()

    assert kernel._context.app is not None
