from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_owns_single_runtime_instance(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should own single runtime graph instance.
    """
    runtime_a = kernel_harness.kernel.runtime
    runtime_b = kernel_harness.kernel.runtime

    assert runtime_a is runtime_b


def test_kernel_context_owns_single_runtime_instance(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Context should preserve stable runtime identity.
    """
    runtime_a = kernel_harness.kernel.context.runtime
    runtime_b = kernel_harness.kernel.context.runtime

    assert runtime_a is runtime_b


def test_kernel_harness_owns_single_kernel(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Harness should preserve stable kernel identity.
    """
    kernel_a = kernel_harness.kernel
    kernel_b = kernel_harness.kernel

    assert kernel_a is kernel_b


def test_kernel_runtime_domains_are_owned_by_runtime(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime graph should own all runtime domains.
    """
    runtime = kernel_harness.kernel.runtime

    assert runtime.lifecycle is not None
    assert runtime.infrastructure is not None
    assert runtime.messaging is not None
    assert runtime.transports is not None
    assert runtime.modules is not None


def test_kernel_is_runtime_owner(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should remain the runtime owner boundary.
    """
    assert (
        kernel_harness.kernel.context.runtime
        is kernel_harness.kernel.runtime
    )
