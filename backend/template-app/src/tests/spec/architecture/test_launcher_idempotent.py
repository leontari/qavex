from template_app.launcher.config import (
    LauncherConfig,
)
from template_app.launcher.run import (
    KernelLauncher,
)


def test_build_returns_same_composition():

    launcher = KernelLauncher(
        LauncherConfig(),
    )

    first = launcher.build()
    second = launcher.build()

    assert first is second
