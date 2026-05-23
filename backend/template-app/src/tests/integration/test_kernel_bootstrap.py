from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_bootstrap_returns_kernel() -> None:
    kernel = bootstrap_kernel()

    assert kernel is not None


def test_bootstrap_creates_fastapi() -> None:
    kernel = bootstrap_kernel()

    assert isinstance(kernel.app, FastAPI)


def test_bootstrap_binds_lifespan() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.app.router.lifespan_context
        is not None
    )
