from runtime.container.providers import ScopedProvider
from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace


class RequestContext:
    pass


def test_scoped_provider() -> None:
    manager = DependencyManager()

    manager.register(
        RequestContext,
        ScopedProvider(lambda _: RequestContext()),
        namespace=Namespace("kernel"),
    )

    scope = manager.create_scope()

    a = manager.resolve(
        RequestContext,
        scope_id=scope.id,
    )

    b = manager.resolve(
        RequestContext,
        scope_id=scope.id,
    )

    assert a is b
