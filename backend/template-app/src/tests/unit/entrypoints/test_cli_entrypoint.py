from __future__ import annotations

from unittest.mock import MagicMock

from template_app.cli import main


def test_cli_main_bootstraps_kernel(monkeypatch) -> None:
    """CLI entrypoint must bootstrap runtime kernel."""

    launcher_mock = MagicMock()

    monkeypatch.setattr(
        "template_app.cli.bootstrap_kernel",
        lambda: "kernel",
    )

    monkeypatch.setattr(
        "template_app.cli.parse_launcher_config",
        lambda: "config",
    )

    monkeypatch.setattr(
        "template_app.cli.KernelLauncher",
        lambda **kwargs: launcher_mock,
    )

    main()

    launcher_mock.run.assert_called_once()
