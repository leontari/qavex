from fastapi import FastAPI

from template_app.runtime.transports.http.factory import (
    create_http_app,
)
from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)
from tests.factories.kernel import (
    build_kernel_no_transport,
)


def test_fastapi_transport_creates_app() -> None:
    kernel = build_kernel_no_transport()

    app = create_http_app(
        kernel,
    )

    assert isinstance(
        app,
        FastAPI,
    )


def test_fastapi_transport_installed_into_kernel() -> None:
    kernel = build_kernel_no_transport()

    create_http_app(
        kernel,
    )

    transport = kernel.transport_manager.get(
        FastAPITransport,
    )

    assert transport is not None
