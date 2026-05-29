from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_boots_without_transports(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should boot without any installed transports.

    Runtime kernel must remain transport-agnostic.
    """
    assert kernel_harness.kernel is not None


def test_kernel_has_no_transports_by_default(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime kernel should not install transports implicitly.
    """
    assert kernel_harness.kernel.transports == ()


def test_transport_manager_starts_empty(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport manager should start without transports.
    """
    manager = kernel_harness.kernel.transport_manager

    assert manager.transports == ()


def test_transport_runtime_starts_empty(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport runtime domain should start empty.
    """
    transport_runtime = kernel_harness.kernel.transport_runtime

    assert transport_runtime.manager.transports == ()


def test_kernel_does_not_depend_on_http_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should not depend on HTTP runtime existence.
    """
    runtime = kernel_harness.kernel.runtime

    assert runtime.transports is not None


def test_kernel_context_exists_without_transports(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel context should exist independently
    from transport layer.
    """
    assert kernel_harness.kernel.context is not None


def test_runtime_domains_exist_without_transports(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Runtime domains should boot
    independently from transports.
    """
    kernel = kernel_harness.kernel

    assert kernel.lifecycle is not None
    assert kernel.infrastructure is not None
    assert kernel.messaging is not None
    assert kernel.module_runtime is not None


def test_kernel_transport_boundary_is_optional(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Transport layer should remain optional boundary.
    """
    assert len(kernel_harness.kernel.transports) == 0
