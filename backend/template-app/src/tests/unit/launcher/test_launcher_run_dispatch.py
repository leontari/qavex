from unittest.mock import Mock

from template_app.launcher.run import KernelLauncher
from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode


def test_launcher_dispatch_http(monkeypatch) -> None:
    kernel = Mock()

    launcher = KernelLauncher(
        _kernel=kernel,
        _config=LauncherConfig(mode=LaunchMode.HTTP),
    )

    called = {}

    monkeypatch.setattr(
        "template_app.launcher.run.KernelLauncher._run_http",
        lambda self: called.setdefault("http", True),
    )

    launcher.run()

    assert called["http"] is True
