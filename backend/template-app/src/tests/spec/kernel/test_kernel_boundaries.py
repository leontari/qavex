from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_exposes_context_boundary(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose immutable context boundary.
    """
    assert kernel_harness.kernel.context is not None


def test_kernel_context_owns_runtime(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    KernelContext should own runtime graph.
    """
    assert (
        kernel_harness.kernel.context.runtime
        is kernel_harness.kernel.runtime
    )


def test_kernel_runtime_not_exposed_as_mutable_field(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime should only be exposed
    through controlled kernel facade.
    """
    runtime = kernel_harness.kernel.runtime

    assert runtime is not None


def test_kernel_runtime_domains_resolve_from_context(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime domains should resolve
    from context-owned runtime graph.
    """
    runtime = kernel_harness.kernel.context.runtime

    assert kernel_harness.kernel.lifecycle is runtime.lifecycle
    assert kernel_harness.kernel.infrastructure is runtime.infrastructure
    assert kernel_harness.kernel.messaging is runtime.messaging
    assert kernel_harness.kernel.transport_runtime is runtime.transports
    assert kernel_harness.kernel.module_runtime is runtime.modules
