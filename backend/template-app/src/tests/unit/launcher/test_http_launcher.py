from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_launcher_installs_http_transport() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    composition = launcher.build()

    transport = composition.kernel.transport_manager.get(FastAPITransport)

    assert transport is not None


def test_http_launcher_freezes_kernel() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True
