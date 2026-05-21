from __future__ import annotations

from fastapi import FastAPI

from tests.factories.kernel import (
    build_testing_kernel,
)


def test_testing_kernel_builds_initialized_runtime() -> None:
    kernel = build_testing_kernel()

    assert kernel.context.runtime is not None


def test_testing_app_returns_fastapi_instance() -> None:

    kernel = build_testing_kernel()

    assert isinstance(kernel.app, FastAPI)
