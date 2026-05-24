from tests.factories.kernel import (
    build_kernel_no_transport,
)
from template_app.transports.http.fastapi_transport import (
    FastAPITransport,
)


def test_kernel_has_no_http_transport_by_default() -> None:
    kernel = build_kernel_no_transport()

    transport = kernel.transport_manager.get(
        FastAPITransport,
    )

    assert transport is None


def test_kernel_starts_without_transports() -> None:
    kernel = build_kernel_no_transport()

    assert kernel.transports == ()
