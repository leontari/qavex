from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_exposes_lifecycle_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose lifecycle runtime domain facade.
    """
    assert kernel.lifecycle is kernel.context.runtime.lifecycle


def test_kernel_exposes_infrastructure_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose infrastructure runtime domain facade.
    """
    assert kernel.infrastructure is kernel.context.runtime.infrastructure


def test_kernel_exposes_messaging_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose messaging runtime domain facade.
    """
    assert kernel.messaging is kernel.context.runtime.messaging


def test_kernel_exposes_transport_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose transport runtime domain facade.
    """
    assert kernel.transport_runtime is kernel.context.runtime.transports


def test_kernel_exposes_module_runtime_domain(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel should expose module runtime domain facade.
    """
    assert kernel.module_runtime is kernel.context.runtime.modules
