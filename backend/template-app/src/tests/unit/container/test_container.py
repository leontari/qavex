from template_app.runtime.container.container import Container
from template_app.runtime.container.providers import FactoryProvider
from template_app.runtime.container.providers import SingletonProvider


class Service:
    pass


def test_singleton_provider():

    container = Container()

    container.register(
        Service,
        SingletonProvider(
            lambda c: Service(),
        ),
    )

    first = container.resolve(Service)
    second = container.resolve(Service)

    assert first is second


def test_factory_provider():

    container = Container()

    container.register(
        Service,
        FactoryProvider(
            lambda c: Service(),
        ),
    )

    first = container.resolve(Service)
    second = container.resolve(Service)

    assert first is not second


def test_namespaces():

    class UsersService:
        pass

    class BillingService:
        pass

    container = Container()

    container.register(
        UsersService,
        SingletonProvider(
            lambda c: UsersService(),
        ),
        namespace="users",
    )

    container.register(
        BillingService,
        SingletonProvider(
            lambda c: BillingService(),
        ),
        namespace="billing",
    )

    assert container.resolve(
        UsersService,
        "users",
    )

    assert container.resolve(
        BillingService,
        "billing",
    )


def test_try_resolve():

    container = Container()

    assert container.try_resolve(Service) is None
