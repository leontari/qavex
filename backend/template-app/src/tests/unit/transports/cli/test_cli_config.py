from template_app.transports.cli.config import CLITransportConfig


def test_cli_config_defaults() -> None:
    cfg = CLITransportConfig()

    assert cfg.interactive is True
    assert cfg.verbose is False
