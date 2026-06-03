from __future__ import annotations

from unittest.mock import Mock

from template_app.launcher import facade


def test_run_http_uses_http_mode(monkeypatch) -> None:
    launcher = Mock()

    monkeypatch.setattr(
        facade,
        "KernelLauncher",
        lambda cfg: launcher,
    )

    facade.run_cli()

    launcher.run.assert_called_once()
