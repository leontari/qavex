from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_bootstrap_returns_kernel() -> None:
    kernel = bootstrap_application()

    assert kernel is not None


def test_bootstrap_creates_fastapi() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel.app, FastAPI)


def test_bootstrap_binds_lifespan() -> None:
    kernel = bootstrap_application()

    assert (
        kernel.app.router.lifespan_context
        is not None
    )
