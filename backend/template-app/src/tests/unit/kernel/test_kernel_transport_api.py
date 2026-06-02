from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.manager import TransportManager


def test_kernel_exposes_transport_manager(kernel: RuntimeKernel) -> None:
    assert isinstance(kernel.transport_manager, TransportManager)


def test_kernel_transport_manager_belongs_to_runtime(kernel: RuntimeKernel) -> None:
    assert kernel.transport_manager is kernel.transport_runtime.manager


def test_kernel_transport_snapshot_is_tuple(kernel: RuntimeKernel) -> None:
    assert isinstance(kernel.transports, tuple)


def test_kernel_transport_runtime_exposes_manager(kernel: RuntimeKernel) -> None:
    assert kernel.transport_runtime.manager is kernel.transport_manager


def test_kernel_transport_manager_is_stable(kernel: RuntimeKernel) -> None:
    assert kernel.transport_manager is kernel.transport_manager
