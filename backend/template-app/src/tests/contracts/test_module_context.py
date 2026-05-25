from __future__ import annotations

from template_app.runtime.kernel.bootstrap import  bootstrap_kernel


def test_module_context_created() -> None:
    kernel = bootstrap_kernel()

    assert kernel._context.app is not None
