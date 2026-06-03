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

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.kernel.kernel import RuntimeKernel



class KernelTestHarness:
    """
    Unifies runtime-aware testing entrypoint.

    Responsibilities:
        - test environment bootstrap

    This is the ONLY valid kernel creation entrypoint in tests.
    """

    def __init__(self, mode: LaunchMode = LaunchMode.HTTP) -> None:
        launcher = KernelLauncher(LauncherConfig(mode = mode))
        composition = launcher.build()

        self._kernel = composition.kernel

    @property
    def kernel(self) -> RuntimeKernel:
        """Return SUT."""
        return self._kernel
