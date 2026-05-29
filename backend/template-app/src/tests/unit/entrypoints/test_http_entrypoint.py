from __future__ import annotations

from unittest.mock import MagicMock

from template_app.http_ import main
from template_app.launcher.modes import LaunchMode


def test_http_entrypoint_runs_launcher(monkeypatch) -> None:
    """
    HTTP entrypoint must run launcher.
    """

    launcher_mock = MagicMock()

    monkeypatch.setattr(
        "template_app.http_.bootstrap_kernel",
        lambda: "kernel",
    )

    monkeypatch.setattr(
        "template_app.http_.KernelLauncher",
        lambda **kwargs: launcher_mock,
    )

    captured = {}

    def fake_config(mode):
        captured["mode"] = mode
        return "config"

    monkeypatch.setattr(
        "template_app.http_.LauncherConfig",
        fake_config,
    )

    main()

    assert captured["mode"] == LaunchMode.HTTP

    launcher_mock.run.assert_called_once()
