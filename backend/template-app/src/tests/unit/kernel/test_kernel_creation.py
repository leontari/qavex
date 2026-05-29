from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_harness_bootstraps_kernel(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Harness must bootstrap runtime kernel.

    Responsibilities:
        - single source of truth
        - runtime ownership
        - kernel orchestration
    """
    assert kernel_harness.kernel is not None


def test_kernel_harness_exposes_kernel_context(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Harness should expose immutable kernel context boundary.
    """
    assert kernel_harness.kernel.context is not None


def test_kernel_harness_exposes_runtime_via_context(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime must be accessed through kernel context boundary.

    Architecture:
        RuntimeKernel
            -> KernelContext
                -> RuntimeState
    """
    runtime = kernel_harness.kernel.context.runtime

    assert runtime is not None


def test_kernel_runtime_property_maps_to_context_runtime(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel.runtime should proxy context.runtime.
    """
    assert (
        kernel_harness.kernel.runtime
        is kernel_harness.kernel.context.runtime
    )


def test_kernel_context_is_immutable(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel context should be immutable boundary object.
    """
    context = kernel_harness.kernel.context

    assert hasattr(context, "runtime")

    try:
        context.runtime = None

    except Exception:
        assert True

    else:
        assert False, "KernelContext must be immutable."
