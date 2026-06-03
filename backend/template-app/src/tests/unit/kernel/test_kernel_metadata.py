from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_exposes_metadata(kernel: RuntimeKernel) -> None:
    assert kernel.metadata is not None
