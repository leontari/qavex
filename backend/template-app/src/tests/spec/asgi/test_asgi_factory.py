from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.http.factory import create_http_app


def test_http_factory_returns_fastapi(kernel: RuntimeKernel) -> None:
    app = create_http_app(kernel)

    assert isinstance(app, FastAPI)


def test_http_factory_does_not_install_transport(
    kernel: RuntimeKernel
) -> None:
    create_http_app(kernel)

    assert len(kernel.transports) == 0
