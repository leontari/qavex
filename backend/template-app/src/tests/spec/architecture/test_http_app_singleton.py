from template_app.launcher.config import LauncherConfig
from template_app.launcher.run import KernelLauncher


def test_http_app_not_rebuilt():
    launcher = KernelLauncher(
        LauncherConfig(),
    )

    app1 = launcher.build_http_app()
    app2 = launcher.build_http_app()

    assert app1 is app2
