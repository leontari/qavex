from __future__ import annotations

from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_kernel_owns_runtime_graph(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must be the single owner of RuntimeState graph.
    """
    kernel = kernel_harness.kernel

    assert kernel.runtime is not None


def test_kernel_runtime_graph_is_accessed_through_context(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime graph must be reachable through KernelContext boundary.
    """
    kernel = kernel_harness.kernel

    assert (
        kernel.context.runtime
        is kernel.runtime
    )


def test_kernel_context_is_immutable_boundary(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    KernelContext must be immutable runtime boundary.
    """
    context = kernel_harness.kernel.context

    assert getattr(context, "__dataclass_params__").frozen is True


def test_kernel_runtime_graph_is_single_source_of_truth(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    RuntimeState must not be duplicated inside kernel.
    """
    kernel = kernel_harness.kernel

    assert kernel.runtime is kernel.context.runtime


def test_kernel_does_not_expose_duplicate_runtime_instances(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must not create multiple runtime graph instances.
    """
    kernel = kernel_harness.kernel

    assert (
        id(kernel.runtime)
        == id(kernel.context.runtime)
    )


def test_runtime_graph_is_not_exposed_directly_as_kernel_state(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel must not duplicate runtime state.
    """
    kernel = kernel_harness.kernel

    assert hasattr(kernel, "runtime")
    assert kernel.runtime is kernel.context.runtime
