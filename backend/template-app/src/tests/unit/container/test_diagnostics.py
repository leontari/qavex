from __future__ import annotations

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Database:
    pass


class Cache:
    pass


def test_snapshot_contains_registered_nodes() -> None:
    manager = DependencyManager()

    manager.register(
        Database,
        SingletonProvider(
            lambda _: Database(),
        ),
        namespace="infrastructure",
    )

    graph = manager.snapshot()

    assert len(graph.nodes) == 1

    node = graph.nodes[0]

    assert node.contract == "Database"

    assert node.namespace == "infrastructure"


def test_dump_contains_contract_names() -> None:
    manager = DependencyManager()

    manager.register(
        Database,
        SingletonProvider(
            lambda _: Database(),
        ),
        namespace="infrastructure",
    )

    manager.register(
        Cache,
        SingletonProvider(
            lambda _: Cache(),
        ),
        namespace="infrastructure",
    )

    dump = manager.dump()

    assert "Database" in dump

    assert "Cache" in dump

    assert "infrastructure" in dump
