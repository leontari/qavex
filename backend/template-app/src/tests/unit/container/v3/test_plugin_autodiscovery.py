from runtime.container.plugin import PluginLoader


def test_autodiscovery() -> None:
    loader = PluginLoader()

    plugins = loader.discover("tests.fake_plugins")

    assert plugins
