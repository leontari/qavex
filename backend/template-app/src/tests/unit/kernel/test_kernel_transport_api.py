from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.manager import TransportManager
from tests.support.fakes.transports import FakeTransport


def test_kernel_exposes_transport_manager(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose runtime transport manager.
    """
    manager = kernel.transport_manager

    assert isinstance(manager, TransportManager)


def test_kernel_transport_manager_belongs_to_runtime(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel transport manager should resolve
    from runtime transport domain.
    """
    assert kernel.transport_manager is kernel.transport_runtime.manager


def test_kernel_exposes_transport_installation_api(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should support transport installation.
    """
    transport = FakeTransport()

    kernel.install_transport(transport)

    assert transport in kernel.transports


def test_kernel_transport_snapshot_contains_installed_transport(
    kernel: RuntimeKernel,
) -> None:
    """
    Installed transports should appear
    in immutable transport snapshot.
    """
    transport = FakeTransport()

    kernel.install_transport(transport)

    transports = kernel.transports

    assert transport in transports


def test_kernel_transport_manager_resolves_transport(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport manager should resolve installed transport.
    """
    transport = FakeTransport()

    kernel.install_transport(transport)

    resolved = kernel.transport_manager.get(FakeTransport)

    assert resolved is transport


def test_kernel_transport_snapshot_is_tuple(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel transport snapshot should remain immutable.
    """
    assert isinstance(kernel.transports, tuple)


def test_kernel_transport_runtime_exposes_manager(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport runtime should expose transport manager.
    """
    transport_runtime = kernel.transport_runtime

    assert transport_runtime.manager is kernel.transport_manager


def test_kernel_transport_installation_updates_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport installation should update runtime domain.
    """
    transport = FakeTransport()

    kernel.install_transport(transport)

    assert transport in kernel.transports


def test_kernel_transport_manager_preserves_identity(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should preserve stable manager identity.
    """
    manager_a = kernel.transport_manager
    manager_b = kernel.transport_manager

    assert manager_a is manager_b


def test_kernel_transport_manager_access(kernel: RuntimeKernel) -> None:
    """
    Kernel must expose transport manager.
    """
    assert kernel.transport_manager is kernel.runtime.transports.manager
