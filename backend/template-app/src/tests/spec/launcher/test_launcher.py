from __future__ import annotations

from unittest.mock import patch

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher


@patch("template_app.runtime.transports.http.entrypoint.run_http_runtime")
def test_launcher_dispatches_http_mode(
    mocked_runtime,
) -> None:
    launcher = KernelLauncher(
        _config=LauncherConfig(
            mode=LaunchMode.HTTP
        )
    )

    launcher.run()

    mocked_runtime.assert_called_once()


@patch("template_app.runtime.transports.cli.entrypoint.run_cli_runtime")
def test_launcher_dispatches_cli_mode(
    mocked_runtime,
) -> None:
    launcher = KernelLauncher(
        _config=LauncherConfig(
            mode=LaunchMode.CLI,
        ),
    )

    launcher.run()

    mocked_runtime.assert_called_once()
