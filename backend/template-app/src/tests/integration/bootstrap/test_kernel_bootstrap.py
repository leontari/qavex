from __future__ import annotations

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_bootstrap_returns_kernel() -> None:
    kernel = bootstrap_kernel()

    assert kernel is not None
