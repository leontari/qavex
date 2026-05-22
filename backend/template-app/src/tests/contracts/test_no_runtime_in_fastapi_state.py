from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_runtime_not_stored_inside_fastapi_state() -> None:
    kernel = bootstrap_application()

    assert not hasattr(kernel._context.app.state, "context")
    assert not hasattr(kernel.app.state, "runtime",)
    assert not hasattr(kernel.app.state, "kernel")
