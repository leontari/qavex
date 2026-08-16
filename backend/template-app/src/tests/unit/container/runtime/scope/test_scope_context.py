import asyncio

import pytest

from template_app.runtime.container.runtime.dependency import DependencyID
from template_app.runtime.container.runtime.scope import (
    ScopeContext,
    ScopeState,
    ScopeID,
)


def test_scope_defaults(scope_id: ScopeID) -> None:
    scope = ScopeContext(id=scope_id)

    assert scope.id == scope_id
    assert scope.state is ScopeState.ACTIVE
    assert scope.owner_id is None
    assert scope.parent_scope is None
    assert scope.count == 0
    assert scope.future_count == 0


def test_contains_set_get(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    service = object()
    scope.set(dependency_id, service)

    assert scope.contains(dependency_id)
    assert scope.get(dependency_id) is service


def test_contains_false(
    scope_context: ScopeContext,
    dependency_id: DependencyID
) -> None:
    assert not scope_context.contains(dependency_id)


def test_set_and_get_instance(
    scope_context: ScopeContext,
    dependency_id: DependencyID
) -> None:
    instance = object()
    scope_context.set(dependency_id, instance)

    assert scope_context.contains(dependency_id)
    assert scope_context.get(dependency_id) is instance


def test_get_missing_raises(
    scope_context: ScopeContext,
    dependency_id: DependencyID
) -> None:
    with pytest.raises(KeyError):
        scope_context.get(dependency_id)


def test_clear_removes_everything(
    scope_context: ScopeContext,
    dependency_id: DependencyID
) -> None:
    scope_context.set(dependency_id, object())
    scope_context.set_future(dependency_id, asyncio.Future())
    scope_context.clear()

    assert not scope_context.instances
    assert scope_context.get_future(dependency_id) is None


def test_remove_instance(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    scope.set(dependency_id, object())
    scope.remove(dependency_id)

    assert not scope.contains(dependency_id)


def test_future_lifecycle(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    future = asyncio.Future()
    scope.set_future(dependency_id, future)

    assert scope.contains_future(dependency_id)
    assert scope.get_future(dependency_id) is future

    scope.remove_future(dependency_id)

    assert not scope.contains_future(dependency_id)


def test_iter_futures(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    future = asyncio.Future()
    scope.set_future(dependency_id, future)
    futures = list(scope.iter_futures())

    assert futures == [future]


def test_clear(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    scope.set(dependency_id, object())
    scope.set_future(dependency_id, asyncio.Future())

    scope.clear()

    assert scope.count == 0
    assert scope.future_count == 0


def test_instances_view_is_read_only(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    scope.set(dependency_id, object())

    view = scope.instances

    assert dependency_id in view


def test_futures_view_is_read_only(
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope = ScopeContext(id=scope_id)
    scope.set_future(dependency_id, asyncio.Future())

    view = scope.futures

    assert dependency_id in view


def test_get_or_create_future_reuses_existing(
    scope_id: ScopeID,
    dependency_id: DependencyID,
) -> None:
    scope = ScopeContext(id=scope_id)
    loop = asyncio.new_event_loop()

    future1, created1 = scope.get_or_create_future(dependency_id, loop=loop)
    future2, created2 = scope.get_or_create_future(dependency_id, loop=loop)

    assert created1 is True
    assert created2 is False
    assert future1 is future2

    loop.close()


def test_contains_future(
    scope_id: ScopeID,
    dependency_id: DependencyID,
) -> None:
    scope = ScopeContext(id=scope_id)
    future = asyncio.Future()
    scope.set_future(dependency_id, future)

    assert scope.contains_future(dependency_id)


def test_remove_future_missing(
    scope_id: ScopeID,
    dependency_id: DependencyID,
) -> None:
    scope = ScopeContext(id=scope_id)
    scope.remove_future(dependency_id)

    assert scope.future_count == 0


def test_owner_metadata(scope_id):
    scope = ScopeContext(
        id=scope_id,
        owner_id="plugin-a",
    )

    assert scope.owner_id == "plugin-a"


def test_parent_metadata(scope_id):
    parent = scope_id

    child = ScopeContext(
        id=scope_id,
        parent_scope=parent,
    )

    assert child.parent_scope == parent


def test_futures_view(
    scope_id: ScopeID,
    dependency_id: DependencyID,
) -> None:
    scope = ScopeContext(id=scope_id)
    future = asyncio.Future()
    scope.set_future(dependency_id, future)
    view = scope.futures

    assert dependency_id in view
    assert view[dependency_id] is future


def test_future_count(
    scope_id: ScopeID,
    dependency_id: DependencyID,
) -> None:
    scope = ScopeContext(id=scope_id)

    scope.set_future(
        dependency_id,
        asyncio.Future(),
    )

    assert scope.future_count == 1
