from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_lifespan_registered_after_kernel_creation() -> None:
    kernel = bootstrap_application()

    assert (
        kernel.app.router.lifespan_context
        is not None
    )
