from __future__ import annotations

from tests.factories.kernel import build_testing_kernel


def test_runtime_not_stored_in_fastapi_state() -> None:
    kernel = build_testing_kernel()

    assert not hasattr(kernel.app.state, "runtime")
    assert not hasattr(kernel.app.state, "kernel")
    assert not hasattr(kernel.app.state, "context")
