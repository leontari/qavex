from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel


def test_kernel_context_is_immutable(kernel: RuntimeKernel) -> None:
    """
    Kernel context should be immutable boundary object.
    """
    context = kernel.context

    assert hasattr(context, "runtime")

    try:
        context.runtime = None

    except Exception:
        assert True

    else:
        assert False, "KernelContext must be immutable."
