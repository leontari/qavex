from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_kernel_always_contains_initialized_app() -> None:
    kernel = bootstrap_application()

    assert kernel.app is not None
