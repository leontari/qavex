from __future__ import annotations

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_kernel_always_contains_initialized_app() -> None:
    kernel = bootstrap_kernel()

    assert kernel.app is not None
