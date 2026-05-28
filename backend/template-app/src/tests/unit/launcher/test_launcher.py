from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from tests.support.factories.kernel import build_kernel_no_transport


def test_launcher_created() -> None:
    launcher = KernelLauncher(
        _kernel=build_kernel_no_transport(),
        _config=LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    assert launcher is not None
