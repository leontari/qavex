"""Kernel specific asserts."""

from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def assert_kernel_frozen(kernel: RuntimeKernel) -> None:
    assert kernel.is_frozen is True


def assert_kernel_mutable(kernel: RuntimeKernel) -> None:
    assert kernel.is_frozen is False
