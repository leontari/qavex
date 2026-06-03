from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_transport_installed():
    launcher = KernelLauncher(LauncherConfig(mode=LaunchMode.HTTP))
    composition = launcher.build()
    transport = composition.kernel.transport_manager.get(FastAPITransport)

    assert transport is not None
