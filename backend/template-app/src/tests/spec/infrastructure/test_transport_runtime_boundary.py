from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.http.factory import FastAPITransport


def test_kernel_has_http_transport_by_default(
    kernel: RuntimeKernel,
) -> None:

    transport = kernel.transport_manager.get(FastAPITransport)

    assert transport is not None
    assert isinstance(transport, FastAPITransport)


# def test_kernel_starts_without_transports() -> None:
#     kernel = build_kernel_no_transport()
#
#     assert kernel.transports == ()
