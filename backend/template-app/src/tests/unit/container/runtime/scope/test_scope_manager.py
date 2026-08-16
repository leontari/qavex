import asyncio

import pytest

from template_app.runtime.container.exceptions import ScopeNotFoundError
from template_app.runtime.container.runtime.dependency import DependencyID
from template_app.runtime.container.runtime.scope import (
    ScopeID,
    ScopeState,
    ScopeManager,
)


def test_create_scope(scope_manager: ScopeManager, scope_id: ScopeID)  -> None:
    scope_id = scope_manager.create_scope()

    assert scope_manager.exists(scope_id)


def test_get_scope(scope_manager: ScopeManager, scope_id: ScopeID) -> None:
    scope_id = scope_manager.create_scope()
    scope = scope_manager.get_scope(scope_id)

    assert scope.id == scope_id


def test_close_scope(scope_manager: ScopeManager, scope_id: ScopeID) -> None:
    scope_id = scope_manager.create_scope()
    scope_manager.close_scope(scope_id)

    assert not scope_manager.exists(scope_id)


def test_close_scope_cancels_futures(
    scope_manager: ScopeManager,
    dependency_id: DependencyID,
    scope_id: ScopeID
) -> None:
    scope_id = scope_manager.create_scope()
    scope = scope_manager.get_scope(scope_id)

    future = asyncio.Future()

    scope.set_future(dependency_id, future)
    scope_manager.close_scope(scope_id)

    assert future.cancelled()


def test_get_unknown_scope_raises(
    scope_manager: ScopeManager,
    scope_id: ScopeID,
) -> None:

    with pytest.raises(ScopeNotFoundError):
        scope_manager.get_scope(scope_id)


def test_scopes_count(scope_manager: ScopeManager) -> None:
    first = scope_manager.create_scope()
    second = scope_manager.create_scope()

    assert scope_manager.scopes_count == 2

    scope_manager.close_scope(first)
    scope_manager.close_scope(second)

    assert scope_manager.scopes_count == 0


def test_close_owner_scopes(scope_manager: ScopeManager) -> None:
    scope1 = scope_manager.create_scope(owner_id="plugin-a")
    scope2 = scope_manager.create_scope(owner_id="plugin-a")
    scope3 = scope_manager.create_scope(owner_id="plugin-b")
    scope_manager.close_owner_scopes("plugin-a")

    assert not scope_manager.exists(scope1)
    assert not scope_manager.exists(scope2)
    assert scope_manager.exists(scope3)


def test_parent_scope_metadata(scope_manager: ScopeManager) -> None:
    parent = scope_manager.create_scope()
    child = scope_manager.create_scope(parent_scope=parent)
    scope = scope_manager.get_scope(child)

    assert scope.parent_scope == parent


def test_active_scopes(scope_manager: ScopeManager) -> None:
    scope1 = scope_manager.create_scope()
    scope2 = scope_manager.create_scope()
    active = scope_manager.active_scopes

    assert scope1 in active
    assert scope2 in active

def test_scope_contexts(scope_manager: ScopeManager) -> None:
    scope_id = scope_manager.create_scope()
    contexts = scope_manager.scope_contexts

    assert scope_id in contexts


def test_snapshots(scope_manager: ScopeManager) -> None:
    scope_id = scope_manager.create_scope(
        owner_id="plugin-a",
    )
    snapshots = scope_manager.snapshots

    assert len(snapshots) == 1

    snapshot = snapshots[0]

    assert snapshot.id == scope_id
    assert snapshot.state is ScopeState.ACTIVE
    assert snapshot.owner_id == "plugin-a"


def test_scope_state_transition(scope_manager: ScopeManager) -> None:
    scope_id = scope_manager.create_scope()
    scope = scope_manager.get_scope(scope_id)

    assert scope.state is ScopeState.ACTIVE

    scope_manager.close_scope(scope_id)

    assert not scope_manager.exists(scope_id)


def test_nested_scope_metadata(scope_manager: ScopeManager) -> None:
    parent = scope_manager.create_scope()
    child = scope_manager.create_scope(parent_scope=parent)

    scope = scope_manager.get_scope(child)

    assert scope.parent_scope == parent


def test_close_scope_removes_scope(scope_manager: ScopeManager) -> None:
    scope_id = scope_manager.create_scope()
    scope_manager.close_scope(scope_id)

    assert not scope_manager.exists(scope_id)
