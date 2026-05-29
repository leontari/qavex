from __future__ import annotations

from template_app.runtime.transports.manager import TransportManager
from tests.support.fakes.transports import FakeTransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_exposes_transport_manager(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose runtime transport manager.
    """
    manager = kernel_harness.kernel.transport_manager

    assert isinstance(manager, TransportManager)


def test_kernel_transport_manager_belongs_to_runtime(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel transport manager should resolve
    from runtime transport domain.
    """
    assert (
        kernel_harness.kernel.transport_manager
        is kernel_harness.kernel.transport_runtime.manager
    )


def test_kernel_can_install_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should support transport installation.
    """
    transport = FakeTransport()

    kernel_harness.kernel.install_transport(transport)

    assert transport in kernel_harness.kernel.transports


def test_kernel_transport_snapshot_contains_installed_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Installed transports should appear
    in immutable transport snapshot.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    transports = kernel_harness.kernel.transports

    assert transport in transports


def test_kernel_transport_manager_resolves_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport manager should resolve installed transport.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    resolved = kernel_harness.kernel.transport_manager.get(FakeTransport)

    assert resolved is transport


def test_kernel_transport_snapshot_is_tuple(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel transport snapshot should remain immutable.
    """
    assert isinstance(kernel_harness.kernel.transports, tuple)


def test_kernel_transport_runtime_exposes_manager(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport runtime should expose transport manager.
    """
    transport_runtime = kernel_harness.kernel.transport_runtime

    assert transport_runtime.manager is kernel_harness.kernel.transport_manager


def test_kernel_transport_installation_updates_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport installation should update runtime domain.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    assert (
        transport
        in kernel_harness.kernel.transport_runtime.manager.transports
    )


def test_kernel_transport_manager_preserves_identity(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should preserve stable manager identity.
    """
    manager_a = kernel_harness.kernel.transport_manager
    manager_b = kernel_harness.kernel.transport_manager

    assert manager_a is manager_b
