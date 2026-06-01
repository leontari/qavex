from __future__ import annotations

from fastapi import FastAPI

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher


def test_launcher_build_http_app():
    launcher = KernelLauncher(
        _config=LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    app = launcher.build_http_app()

    assert isinstance(app, FastAPI)


def test_build_http_app_returns_fastapi() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    app = launcher.build_http_app()

    assert isinstance(app, FastAPI)
