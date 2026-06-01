from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher


def test_build_returns_same_composition_instance() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    composition1 = launcher.build()
    composition2 = launcher.build()

    assert composition1 is composition2
