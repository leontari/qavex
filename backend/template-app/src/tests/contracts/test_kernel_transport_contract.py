from fastapi import FastAPI

from tests.factories.kernel import build_testing_kernel


def test_kernel_exposes_fastapi_app() -> None:
    kernel = build_testing_kernel()

    assert isinstance(kernel.app, FastAPI)
    assert kernel.app is kernel._context.app
