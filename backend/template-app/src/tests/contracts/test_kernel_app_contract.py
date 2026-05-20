from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_kernel_exposes_fastapi_app() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel.app, FastAPI)
    assert kernel.app is kernel.context.app
