from unittest.mock import Mock

from template_app.runtime.transports.cli.entrypoint import run_cli_runtime


def test_cli_entrypoint_executes(monkeypatch) -> None:
    kernel = Mock()

    monkeypatch.setattr(
        "template_app.transports.cli.entrypoint.build_cli_parser",
        lambda: Mock(parse_args=lambda: Mock(version=False)),
    )

    monkeypatch.setattr(
        "template_app.transports.cli.entrypoint.CLITransport",
        lambda: Mock(),
    )

    run_cli_runtime(kernel)

    kernel.install_transport.assert_called()
    kernel.startup.assert_called()
