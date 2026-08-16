from runtime.container.plugin import Plugin
from runtime.container.graph import DependencyGraph
from runtime.container.namespace import Namespace


class AuthPlugin(Plugin):
    name = "auth"
    namespace = Namespace("plugin.auth")
    requires = ("plugin.database",)
    exports = ()


class DatabasePlugin(Plugin):
    name = "database"
    namespace = Namespace("plugin.database")
    requires = ()
    exports = ()


def test_plugin_dependencies() -> None:
    graph = DependencyGraph()

    graph.add_plugin(AuthPlugin)
    graph.add_plugin(DatabasePlugin)

    graph.validate()
