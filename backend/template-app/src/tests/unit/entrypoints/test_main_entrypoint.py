from __future__ import annotations

from unittest.mock import MagicMock

from template_app.main import main


def test_main_runs_launcher(monkeypatch) -> None:
    launcher = MagicMock()

    monkeypatch.setattr(
        "template_app.main.parse_launcher_config",
        lambda: "config",
    )

    monkeypatch.setattr(
        "template_app.main.KernelLauncher",
        lambda config: launcher,
    )

    main()

    launcher.run.assert_called_once()
