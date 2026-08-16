from runtime.container.providers import SingletonProvider
from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace


class Service:
    pass


def test_singleton_created_once() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(lambda _: Service()),
        namespace=Namespace("kernel"),
    )

    a = manager.resolve(Service)
    b = manager.resolve(Service)

    assert a is b
