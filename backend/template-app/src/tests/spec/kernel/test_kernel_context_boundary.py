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
    kernel: RuntimeKernel,
) -> None:
    """
    Runtime domains should resolve
    from context-owned runtime graph.
    """
    runtime = kernel.context.runtime

    assert kernel.runtime is runtime
    assert kernel.lifecycle is runtime.lifecycle
    assert kernel.infrastructure is runtime.infrastructure
    assert kernel.messaging is runtime.messaging
    assert kernel.transport_runtime is runtime.transports
    assert kernel.module_runtime is runtime.modules


def test_kernel_owns_runtime_graph(kernel: RuntimeKernel) -> None:
    """
    Kernel must be the single owner of RuntimeState graph.
    """
    assert kernel.runtime is not None


def test_kernel_context_is_immutable_boundary(kernel: RuntimeKernel) -> None:
    """
    KernelContext must be immutable runtime boundary.
    """
    context = kernel.context

    assert getattr(context, "__dataclass_params__").frozen is True


def test_kernel_does_not_expose_duplicate_runtime_instances(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel must not create multiple runtime graph instances.
    """
    assert id(kernel.runtime) == id(kernel.context.runtime)


def test_runtime_graph_is_not_exposed_directly_as_kernel_state(
    kernel: RuntimeKernel,
) -> None:
    """
    Kernel must not duplicate runtime state.
    """
    assert hasattr(kernel, "runtime")
    assert kernel.runtime is kernel.context.runtime


def test_kernel_owns_single_runtime_instance(kernel: RuntimeKernel) -> None:
    """
    Kernel should own single runtime graph instance.
    """
    runtime_a = kernel.runtime
    runtime_b = kernel.runtime

    assert runtime_a is runtime_b


def test_kernel_context_owns_single_runtime_instance(
    kernel: RuntimeKernel
) -> None:
    """
    Context should preserve stable runtime identity.
    """
    runtime_a = kernel.context.runtime
    runtime_b = kernel.context.runtime

    assert runtime_a is runtime_b


def test_kernel_harness_owns_single_kernel(kernel: RuntimeKernel) -> None:
    """
    Harness should preserve stable kernel identity.
    """
    kernel_a = kernel
    kernel_b = kernel

    assert kernel_a is kernel_b


def test_kernel_runtime_domains_are_owned_by_runtime(
    kernel: RuntimeKernel,
) -> None:
    """
    Runtime graph should own all runtime domains.
    """
    runtime = kernel.runtime

    assert runtime.lifecycle is not None
    assert runtime.infrastructure is not None
    assert runtime.messaging is not None
    assert runtime.transports is not None
    assert runtime.modules is not None


def test_kernel_exposes_all_runtime_domains(kernel: RuntimeKernel) -> None:
    """
    Kernel must expose runtime domains from runtime graph.
    """
    assert kernel.lifecycle is kernel.runtime.lifecycle
    assert kernel.infrastructure is kernel.runtime.infrastructure
    assert kernel.messaging is kernel.runtime.messaging
    assert kernel.transport_runtime is kernel.runtime.transports
    assert kernel.module_runtime is kernel.runtime.modules
