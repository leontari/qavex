from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_kernel_contains_real_fastapi_app() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel.context.app, FastAPI)
