from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel

from tests.support.fakes.transports import FakeTransport


def test_kernel_rejects_mutation_after_freeze(kernel: RuntimeKernel) -> None:
    """Frozen runtime must reject mutations."""
    kernel.freeze()

    with pytest.raises(RuntimeError):
        kernel.metadata.freeze.ensure_mutable()


def test_kernel_context_is_frozen(kernel: RuntimeKernel) -> None:
    """
    Kernel context must remain immutable.

    Context is the ownership boundary between:
        - RuntimeKernel
        - RuntimeState
    """
    context = kernel.context

    with pytest.raises(Exception):
        context.runtime = None


def test_kernel_exposes_immutable_transport_snapshot(
    kernel: RuntimeKernel
) -> None:
    """
    Kernel should expose immutable transport snapshot.
    """
    kernel.install_transport(FakeTransport())

    transports = kernel.transports

    assert isinstance(transports, tuple)


def test_transport_snapshot_cannot_be_mutated(
    kernel: RuntimeKernel
) -> None:
    """
    Runtime transport snapshot should not support mutation.
    """
    kernel.install_transport(FakeTransport())

    transports = kernel.transports

    with pytest.raises(AttributeError):
        transports.append(FakeTransport())


def test_kernel_modules_snapshot_is_immutable(kernel: RuntimeKernel) -> None:
    """
    Kernel should expose immutable module snapshot.
    """
    modules = kernel.modules

    assert isinstance(modules, tuple)


def test_module_snapshot_cannot_be_mutated(kernel: RuntimeKernel) -> None:
    """
    Runtime module snapshot should not support mutation.
    """
    modules = kernel.modules

    with pytest.raises(AttributeError):
        modules.append(None)


def test_runtime_context_identity_is_stable(kernel: RuntimeKernel) -> None:
    """
    Kernel should preserve stable context identity.
    """
    context_a = kernel.context
    context_b = kernel.context

    assert context_a is context_b


def test_runtime_identity_is_stable(kernel: RuntimeKernel) -> None:
    """
    Kernel should preserve stable runtime identity.
    """
    runtime_a = kernel.runtime
    runtime_b = kernel.runtime

    assert runtime_a is runtime_b


def test_transport_install_allowed_before_freeze(kernel: RuntimeKernel):
    kernel.install_transport(FakeTransport())

    assert len(kernel.transports) == 1


def test_transport_install_forbidden_after_freeze(kernel: RuntimeKernel):
    kernel.freeze()

    with pytest.raises(RuntimeError):
        kernel.install_transport(FakeTransport())


def test_runtime_graph_is_mutable_after_bootstrap(
    kernel: RuntimeKernel
) -> None:
    """
    Bootstrap must not freeze runtime.

    Bootstrap must only create RuntimeKernel.
    Freeze is responsibility of ApplicationBuilder.
    """
    assert kernel.is_frozen is False


def test_install_transport_after_freeze_fails(kernel: RuntimeKernel) -> None:
    kernel.freeze()

    with pytest.raises(RuntimeError):
        kernel.install_transport(FakeTransport())
