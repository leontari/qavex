from __future__ import annotations

from template_app.runtime.kernel import RuntimeKernel
from tests.factories.kernel import build_testing_kernel


def test_bootstrap_returns_kernel() -> None:
    kernel = build_testing_kernel()

    assert isinstance(kernel, RuntimeKernel)
