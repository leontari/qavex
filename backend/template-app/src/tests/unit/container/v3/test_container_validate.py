from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace
from runtime.container.providers import SingletonProvider


class Database:
    pass


def test_validate() -> None:
    manager = DependencyManager()

    manager.register(
        Database,
        SingletonProvider(lambda _: Database()),
        namespace=Namespace("infrastructure.database"),
    )

    manager.validate()
