from template_app.launcher.modes import LaunchMode


def test_launch_modes_exist() -> None:
    assert LaunchMode.HTTP
    assert LaunchMode.KAFKA
    assert LaunchMode.GRPC
    assert LaunchMode.CLI
