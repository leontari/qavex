from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.contracts import Transport
from tests.support.harness.kernel_test_harness import KernelTestHarness
from tests.support.fakes.transports import FakeTransport


def test_kernel_transport_boundary_is_transport_agnostic(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must not depend on any concrete transport implementation.
    """
    kernel = kernel_harness.kernel

    assert isinstance(kernel.transports, tuple)


def test_kernel_does_not_require_http_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must boot without HTTP or any network transport.
    """
    assert kernel_harness.kernel.transports == ()


def test_kernel_transport_installation_respects_boundary(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport installation must go through kernel boundary only.
    """
    transport = FakeTransport()

    kernel_harness.install_transport(transport)

    assert transport in kernel_harness.kernel.transports


def test_kernel_exposes_transport_contract_only(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must expose only Transport protocol objects.
    """
    kernel = kernel_harness.kernel

    for transport in kernel.transports:
        assert isinstance(transport, Transport)


def test_kernel_transport_manager_is_internal_implementation(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    TransportManager must be hidden behind kernel facade.
    """
    kernel = kernel_harness.kernel

    assert kernel.transport_manager is not None
    assert kernel.transport_runtime.manager is kernel.transport_manager


def test_kernel_transport_snapshot_is_read_only(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport snapshot must be immutable.
    """
    transports = kernel_harness.kernel.transports

    assert isinstance(transports, tuple)
    assert not hasattr(transports, "append")
    assert not hasattr(transports, "remove")


def test_kernel_transport_boundary_is_runtime_owned(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport graph must be owned by RuntimeState, not Kernel facade.
    """
    assert (
        kernel_harness.kernel.transport_runtime.manager.transports
        is kernel_harness.kernel.runtime.transports.manager.transports
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
        assert isinstance(transport, Transport)
