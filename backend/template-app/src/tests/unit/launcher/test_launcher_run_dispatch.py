from template_app.launcher.run import KernelLauncher
from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode


def test_launcher_dispatch_http_calls_http_entrypoint(monkeypatch) -> None:
    called = {}

    launcher = KernelLauncher(
        LauncherConfig(mode=LaunchMode.HTTP),
    )

    def fake_http_runtime(*args, **kwargs):
        called["http"] = True

    monkeypatch.setattr(
        "template_app.runtime.transports.http.entrypoint.run_http_runtime",
        fake_http_runtime,
    )

    launcher.run()

    assert called["http"] is True
