from __future__ import annotations

from unittest.mock import MagicMock

from template_app.kafka import main
from template_app.launcher.modes import LaunchMode


def test_kafka_entrypoint_runs_launcher(monkeypatch) -> None:
    """
    Kafka entrypoint must run launcher.
    """

    launcher_mock = MagicMock()

    monkeypatch.setattr(
        "template_app.kafka.bootstrap_kernel",
        lambda: "kernel",
    )

    monkeypatch.setattr(
        "template_app.kafka.KernelLauncher",
        lambda **kwargs: launcher_mock,
    )

    captured = {}

    def fake_config(mode):
        captured["mode"] = mode
        return "config"

    monkeypatch.setattr(
        "template_app.kafka.LauncherConfig",
        fake_config,
    )

    main()

    assert captured["mode"] == LaunchMode.KAFKA

    launcher_mock.run.assert_called_once()
