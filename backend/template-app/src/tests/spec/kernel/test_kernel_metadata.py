from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_contains_metadata(kernel: RuntimeKernel):
    assert kernel.metadata is not None


def test_kernel_contains_descriptor(kernel: RuntimeKernel):
    assert kernel.metadata.descriptor is not None


def test_kernel_contains_capabilities(kernel: RuntimeKernel):
    assert kernel.metadata.capabilities is not None
