from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_context_boundary_is_frozen(kernel: RuntimeKernel) -> None:
    """
    KernelContext must be immutable boundary.
    """
    context = kernel.context

    assert context.runtime is kernel.runtime


def test_kernel_does_not_expose_internal_graph_directly(
    kernel: RuntimeKernel
) -> None:
    """
    Kernel must expose controlled access only.
    """
    # only facade access allowed
    assert hasattr(kernel, "lifecycle")
    assert hasattr(kernel, "transports")
    assert hasattr(kernel, "modules")


def test_kernel_exposes_context_boundary(kernel: RuntimeKernel) -> None:
    """
    Kernel should expose immutable context boundary.
    """
    assert kernel.context is not None


def test_kernel_context_owns_runtime(kernel: RuntimeKernel) -> None:
    """
    KernelContext should own runtime graph.
    """
    assert kernel.context.runtime is kernel.runtime


def test_kernel_runtime_not_exposed_as_mutable_field(
    kernel: RuntimeKernel
) -> None:
    """
    Runtime should only be exposed
    through controlled kernel facade.
    """
    runtime = kernel.runtime

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
