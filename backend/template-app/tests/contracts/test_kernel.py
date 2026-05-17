from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application
from template_app.bootstrap.runtime.kernel import RuntimeKernel


def test_bootstrap_returns_kernel() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel, RuntimeKernel)
