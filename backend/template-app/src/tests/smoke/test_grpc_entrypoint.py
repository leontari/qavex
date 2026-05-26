from template_app.grpc import main


def test_grpc_entrypoint_importable() -> None:
    assert main
