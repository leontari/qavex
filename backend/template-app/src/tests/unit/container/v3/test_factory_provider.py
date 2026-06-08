from runtime.container.providers import FactoryProvider
from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace


class Service:
    pass


def test_factory_returns_new_instance() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        FactoryProvider(lambda _: Service()),
        namespace=Namespace("kernel"),
    )

    a = manager.resolve(Service)
    b = manager.resolve(Service)

    assert a is not b
