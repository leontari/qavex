from __future__ import annotations

from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_kernel_exposes_lifecycle_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose lifecycle runtime domain facade.
    """
    assert (
        kernel_harness.kernel.lifecycle
        is kernel_harness.kernel.context.runtime.lifecycle
    )


def test_kernel_exposes_infrastructure_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose infrastructure runtime domain facade.
    """
    assert (
        kernel_harness.kernel.infrastructure
        is kernel_harness.kernel.context.runtime.infrastructure
    )


def test_kernel_exposes_messaging_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose messaging runtime domain facade.
    """
    assert (
        kernel_harness.kernel.messaging
        is kernel_harness.kernel.context.runtime.messaging
    )


def test_kernel_exposes_transport_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose transport runtime domain facade.
    """
    assert (
        kernel_harness.kernel.transport_runtime
        is kernel_harness.kernel.context.runtime.transports
    )


def test_kernel_exposes_module_runtime_domain(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose module runtime domain facade.
    """
    assert (
        kernel_harness.kernel.module_runtime
        is kernel_harness.kernel.context.runtime.modules
    )
