from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_factory_creates_transport(kernel: RuntimeKernel) -> None:
    app = FastAPI()

    transport = TransportFactory.create_http(kernel=kernel, app=app)

    assert isinstance(transport, FastAPITransport)


def test_factory_does_not_install_transport(kernel: RuntimeKernel) -> None:
    app = FastAPI()

    TransportFactory.create_http(kernel=kernel, app=app)

    assert len(kernel.transports) == 0
