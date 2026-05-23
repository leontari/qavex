from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)



def test_bootstrap_returns_initialized_kernel() -> None:
    kernel = bootstrap_kernel()

    assert isinstance(kernel.app, FastAPI)



def test_kernel_has_runtime_state() -> None:
    kernel = bootstrap_kernel()

    runtime = kernel._context.runtime

    assert runtime.container is not None
    assert runtime.lifecycle_registry is not None
    assert runtime.lifecycle_manager is not None
