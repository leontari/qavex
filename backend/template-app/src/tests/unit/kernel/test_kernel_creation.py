from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_harness_bootstraps_kernel(kernel: RuntimeKernel) -> None:
    """
    Harness must bootstrap runtime kernel.

    Responsibilities:
        - single source of truth
        - runtime ownership
        - kernel orchestration
    """
    assert kernel is not None
    assert isinstance(kernel, RuntimeKernel)


def test_kernel_harness_exposes_kernel_context(
    kernel: RuntimeKernel,
) -> None:
    """
    Harness should expose immutable kernel context boundary.
    """
    assert kernel.context is not None


def test_kernel_harness_exposes_runtime_via_context(
    kernel: RuntimeKernel,
) -> None:
    """
    Runtime must be accessed through kernel context boundary.

    Architecture:
        RuntimeKernel
            -> KernelContext
                -> RuntimeState
    """
    assert kernel.context.runtime is not None


def test_kernel_runtime_property_maps_to_context_runtime(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel.runtime should proxy context.runtime.
    """
    assert kernel.runtime is kernel.context.runtime
