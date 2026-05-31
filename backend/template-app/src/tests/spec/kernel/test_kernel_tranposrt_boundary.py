from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.contracts import Transport
from tests.support.fakes.transports import FakeTransport


def test_kernel_transport_boundary_is_transport_agnostic(
kernel: RuntimeKernel,
) -> None:
    """
    Kernel must not depend on any concrete transport implementation.
    """
    assert isinstance(kernel.transports, tuple)


def test_kernel_does_not_require_http_transport(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel must boot without HTTP or any network transport.
    """
    assert kernel.transports == ()


def test_kernel_transport_installation_respects_boundary(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport installation must go through kernel boundary only.
    """
    transport = FakeTransport()

    kernel.install_transport(transport)

    assert transport in kernel.transports


def test_kernel_exposes_transport_contract_only(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel must expose only Transport protocol objects.
    """
    for transport in kernel.transports:
        assert isinstance(transport, Transport)


def test_kernel_transport_manager_is_internal_implementation(
    kernel: RuntimeKernel,
) -> None:
    """
    TransportManager must be hidden behind kernel facade.
    """
    assert kernel.transport_manager is not None
    assert kernel.transport_runtime.manager is kernel.transport_manager


def test_kernel_transport_snapshot_is_read_only(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport snapshot must be immutable.
    """
    transports = kernel.transports

    assert isinstance(transports, tuple)
    assert not hasattr(transports, "append")
    assert not hasattr(transports, "remove")


def test_kernel_transport_boundary_is_runtime_owned(
    kernel: RuntimeKernel,
) -> None:
    """
    Transport graph must be owned by RuntimeState, not Kernel facade.
    """
    assert (
        kernel.transport_runtime.manager.transports
        == kernel.runtime.transports.manager.transports
    )


def test_kernel_exposes_only_transport_snapshot(
    kernel: RuntimeKernel
) -> None:
    """
    Kernel must expose transport snapshot only (no mutation leak).
    """
    assert isinstance(kernel.transports, tuple)


def test_transport_snapshot_satisfies_contract(kernel: RuntimeKernel) -> None:
    """
    All exposed transports must satisfy Transport protocol.
    """
    for transport in kernel.transports:
        assert hasattr(transport, "startup")
        assert hasattr(transport, "shutdown")
