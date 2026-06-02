from template_app.launcher.run import KernelLauncher
from template_app.launcher.config import LauncherConfig


def test_build_is_idempotent() -> None:
    launcher = KernelLauncher(LauncherConfig())

    first = launcher.build()
    second = launcher.build()

    assert first is second
