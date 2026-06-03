from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode


def test_launcher_config_defaults() -> None:
    config = LauncherConfig()

    assert config.mode == LaunchMode.HTTP


def test_launcher_config_default_mode() -> None:
    config = LauncherConfig()

    assert config.mode == LaunchMode.HTTP


def test_launcher_config_custom_mode() -> None:
    config = LauncherConfig(mode=LaunchMode.CLI)

    assert config.mode == LaunchMode.CLI
