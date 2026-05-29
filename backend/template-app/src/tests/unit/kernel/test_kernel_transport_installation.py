from __future__ import annotations

from tests.support.fakes.transports import FakeTransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_harness_installs_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Harness should install runtime transport
    through kernel orchestration boundary.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    assert transport in kernel_harness.kernel.transports


def test_kernel_harness_resolves_transport_by_type(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Harness should resolve installed transport
    by runtime transport type.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    resolved = kernel_harness.get_transport(FakeTransport)

    assert resolved is transport


def test_kernel_transport_snapshot_is_immutable(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose immutable transport snapshot.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    transports = kernel_harness.kernel.transports

    assert isinstance(transports, tuple)


def test_transport_installation_updates_runtime_manager(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Installing transport through harness
    should update runtime transport manager.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    assert transport in kernel_harness.transports.manager.transports
