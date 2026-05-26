from template_app.http import main


def test_http_entrypoint_importable() -> None:
    assert main
