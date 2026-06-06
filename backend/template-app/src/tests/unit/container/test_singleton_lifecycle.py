from __future__ import annotations

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Database:
    pass


def test_singleton_created_once() -> None:
    manager = DependencyManager()

    manager.register(
        Database,
        SingletonProvider(
            lambda _: Database(),
        ),
    )

    first = manager.resolve(Database)
    second = manager.resolve(Database)

    assert first is second


def test_singleton_cached_after_first_resolve() -> None:
    manager = DependencyManager()

    calls = 0

    def factory(_: object) -> Database:
        nonlocal calls

        calls += 1

        return Database()

    manager.register(
        Database,
        SingletonProvider(factory),
    )

    manager.resolve(Database)
    manager.resolve(Database)
    manager.resolve(Database)

    assert calls == 1
