from tests.support.harness.kernel_test_client import (
    KernelTestClient,
)
from tests.support.fakes.transports import (
    FakeTransport,
)


def test_kernel_can_install_transport(client: KernelTestClient) -> None:
    transport = FakeTransport()

    client.install_transport(transport)

    assert transport in client.kernel.transports


def test_transport_lookup(client: KernelTestClient) -> None:
    transport = FakeTransport()

    client.install_transport(transport)

    resolved = client.get_transport(FakeTransport)

    assert resolved is transport
