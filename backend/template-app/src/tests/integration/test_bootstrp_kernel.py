from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)



def test_bootstrap_returns_initialized_kernel() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel.app, FastAPI)



def test_kernel_has_runtime_state() -> None:
    kernel = bootstrap_application()

    runtime = kernel._context.runtime

    assert runtime.container is not None
    assert runtime.lifecycle_registry is not None
    assert runtime.lifecycle_manager is not None
