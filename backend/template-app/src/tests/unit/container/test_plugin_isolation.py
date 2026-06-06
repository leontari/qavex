from __future__ import annotations

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Service:
    pass


def test_plugin_namespace_isolation() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="plugin.billing",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="plugin.auth",
    )

    billing = manager.resolve(
        Service,
        namespace="plugin.billing",
    )

    auth = manager.resolve(
        Service,
        namespace="plugin.auth",
    )

    assert billing is not auth


def test_same_contract_can_exist_in_multiple_plugins() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="plugin.a",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="plugin.b",
    )

    assert manager.contains(
        Service,
        namespace="plugin.a",
    )

    assert manager.contains(
        Service,
        namespace="plugin.b",
    )
