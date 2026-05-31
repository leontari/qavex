"""
Unified runtime-aware test harness.

Kernel architecture graph:
-------------

RuntimeKernel
    ↓
KernelContext (IMMUTABLE boundary)
    ↓
RuntimeState (mutable runtime graph)
    ↓
domain runtimes (lifecycle / infra / messaging / modules / transports)

"""
from __future__ import annotations

from template_app.runtime.kernel.bootstrap import bootstrap_kernel
from template_app.runtime.kernel.kernel import RuntimeKernel



class KernelTestHarness:
    """
    Unifies runtime-aware testing entrypoint.

    Responsibilities:
        - test environment bootstrap

    This is the ONLY valid kernel creation entrypoint in tests.
    """

    def __init__(self) -> None:
        self._kernel = bootstrap_kernel()

    @property
    def kernel(self) -> RuntimeKernel:
        """Return SUT."""
        return self._kernel
