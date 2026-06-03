from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher


def test_launcher_builds_http_runtime() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen
