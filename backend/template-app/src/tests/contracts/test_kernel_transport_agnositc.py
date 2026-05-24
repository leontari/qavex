from tests.factories.kernel import (
    build_kernel_no_transport,
)


def test_kernel_is_transport_agnostic() -> None:
    kernel = build_kernel_no_transport()

    assert not hasattr(kernel, "app")
    assert not hasattr(kernel, "http_app")
