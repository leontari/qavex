from __future__ import annotations

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    FactoryProvider,
    SingletonProvider,
)


class Service:
    pass


def test_singleton_resolve_returns_same_instance() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="kernel",
    )

    first = manager.resolve(
        Service,
        namespace="kernel",
    )

    second = manager.resolve(
        Service,
        namespace="kernel",
    )

    assert first is second


def test_factory_returns_new_instance() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        FactoryProvider(
            lambda _: Service(),
        ),
        namespace="kernel",
    )

    first = manager.resolve(
        Service,
        namespace="kernel",
    )

    second = manager.resolve(
        Service,
        namespace="kernel",
    )

    assert first is not second


def test_contains() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="kernel",
    )

    assert manager.contains(
        Service,
        namespace="kernel",
    )
