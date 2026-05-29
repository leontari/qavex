from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_kernel_has_no_http_transport_by_default() -> None:
    kernel = bootstrap_kernel()

    assert kernel.transports == ()


def test_kernel_boots_without_transports() -> None:
    kernel = bootstrap_kernel()

    assert kernel is not None
