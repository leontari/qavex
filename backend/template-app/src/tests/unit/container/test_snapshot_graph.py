from __future__ import annotations

from template_app.runtime.container.runtime.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Cache:
    pass


class Database:
    pass


def test_snapshot_contains_all_nodes() -> None:
    manager = DependencyManager()

    manager.register(
        Cache,
        SingletonProvider(
            lambda _: Cache(),
        ),
    )

    manager.register(
        Database,
        SingletonProvider(
            lambda _: Database(),
        ),
    )

    graph = manager.snapshot()

    assert len(graph.nodes) == 2


def test_snapshot_contains_contract_names() -> None:
    manager = DependencyManager()

    manager.register(
        Cache,
        SingletonProvider(
            lambda _: Cache(),
        ),
    )

    graph = manager.snapshot()

    names = {
        node.contract
        for node in graph.nodes
    }

    assert "Cache" in names
