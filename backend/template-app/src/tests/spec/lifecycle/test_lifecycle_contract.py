from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_lifecycle_has_registry(kernel: RuntimeKernel) -> None:
    """
    Lifecycle runtime must expose registry.
    """
    assert kernel.lifecycle.registry is not None
