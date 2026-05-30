import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_runtime_is_frozen_after_bootstrap(kernel: RuntimeKernel) -> None:
    """
    Runtime graph must be frozen after kernel bootstrap.
    """

    assert kernel.runtime.freeze.frozen is True


def test_kernel_rejects_mutation_after_freeze(kernel: RuntimeKernel) -> None:
    """
    Kernel must protect runtime immutability.
    """

    with pytest.raises(RuntimeError):
        kernel.runtime.freeze.ensure_mutable()
