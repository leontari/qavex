from __future__ import annotations

from unittest.mock import MagicMock

from template_app.main import main


def test_main_runs_launcher() -> None:
    launcher = MagicMock()

    with (
        __import__("unittest.mock").mock.patch(
            "template_app.main.parse_launcher_config",
            return_value="config",
        ),
        __import__("unittest.mock").mock.patch(
            "template_app.main.KernelLauncher",
            return_value=launcher,
        ),
    ):
        main()

    launcher.run.assert_called_once()
