from template_app.launcher.config import (
    LauncherConfig,
)
from template_app.launcher.run import (
    KernelLauncher,
)


def test_kernel_is_frozen_after_build():

    launcher = KernelLauncher(
        LauncherConfig(),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True
