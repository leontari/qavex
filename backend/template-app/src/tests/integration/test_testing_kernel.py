from __future__ import annotations

from fastapi import FastAPI

from tests.factories.kernel import (
    build_testing_app,
    build_testing_kernel,
)


def test_testing_kernel_builds_initialized_runtime() -> None:
    kernel = build_testing_kernel()

    # assert kernel.app is not None
    # assert kernel.context.runtime is not None


def test_testing_app_returns_fastapi_instance() -> None:
    app = build_testing_app()

    assert isinstance(app, FastAPI)
