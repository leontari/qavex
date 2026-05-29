from __future__ import annotations

import pytest

from tests.support.fakes.transports import FakeTransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_context_is_frozen(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel context must remain immutable.

    Context is the ownership boundary between:
        - RuntimeKernel
        - RuntimeState
    """
    context = kernel_harness.kernel.context

    with pytest.raises(Exception):
        context.runtime = None


def test_kernel_exposes_immutable_transport_snapshot(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose immutable transport snapshot.
    """
    kernel_harness.install_transport(FakeTransport())

    transports = kernel_harness.kernel.transports

    assert isinstance(transports, tuple)


def test_transport_snapshot_cannot_be_mutated(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime transport snapshot should not support mutation.
    """
    kernel_harness.install_transport(FakeTransport())

    transports = kernel_harness.kernel.transports

    with pytest.raises(AttributeError):
        transports.append(FakeTransport())


def test_kernel_modules_snapshot_is_immutable(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose immutable module snapshot.
    """
    modules = kernel_harness.kernel.modules

    assert isinstance(modules, tuple)


def test_module_snapshot_cannot_be_mutated(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime module snapshot should not support mutation.
    """
    modules = kernel_harness.kernel.modules

    with pytest.raises(AttributeError):
        modules.append(None)


def test_runtime_context_identity_is_stable(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should preserve stable context identity.
    """
    context_a = kernel_harness.kernel.context
    context_b = kernel_harness.kernel.context

    assert context_a is context_b


def test_runtime_identity_is_stable(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should preserve stable runtime identity.
    """
    runtime_a = kernel_harness.kernel.runtime
    runtime_b = kernel_harness.kernel.runtime

    assert runtime_a is runtime_b
