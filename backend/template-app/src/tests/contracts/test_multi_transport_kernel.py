from tests.factories.kernel import build_kernel_no_transport
from tests.fakes.transports import (
    FakeHttpTransport,
    FakeKafkaTransport,
)


def test_kernel_supports_multiple_transports() -> None:
    kernel = build_kernel_no_transport()

    kernel.install_transport(
        FakeHttpTransport(),
    )

    kernel.install_transport(
        FakeKafkaTransport(),
    )

    assert len(kernel.transports) == 2
