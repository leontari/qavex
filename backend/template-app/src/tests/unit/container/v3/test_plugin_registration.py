from runtime.container.plugin import Plugin
from runtime.container.namespace import Namespace


class AuthPlugin(Plugin):

    name = "auth"
    namespace = Namespace("plugin.auth")

    requires = ()

    exports = ()


def test_plugin_metadata() -> None:
    plugin = AuthPlugin()

    assert plugin.name == "auth"
    assert plugin.namespace.name == "plugin.auth"
