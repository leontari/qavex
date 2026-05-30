import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_runtime_graph_cannot_be_mutated_after_freeze(
    kernel: RuntimeKernel
) -> None:
    """
    Runtime graph must reject mutation after freeze.
    """
    with pytest.raises(RuntimeError):
        kernel.runtime.freeze.ensure_mutable()
