from __future__ import annotations

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_lifespan_registered_after_kernel_creation() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.app.router.lifespan_context
        is not None
    )
