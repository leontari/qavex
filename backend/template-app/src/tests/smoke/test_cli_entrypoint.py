from template_app.cli import main


def test_cli_entrypoint_importable() -> None:
    assert main
