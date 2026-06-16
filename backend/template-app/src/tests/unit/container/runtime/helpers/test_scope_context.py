import asyncio

import pytest

from template_app.runtime.container.models.dependency import DependencyID
from template_app.runtime.container.runtime.helpers.context import ScopeContext
from template_app.runtime.container.models.scope import ScopeState, ScopeID


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
