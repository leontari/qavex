import asyncio

import pytest

from template_app.runtime.container.models.dependency import DependencyID
from template_app.runtime.container.models.scope import ScopeID
from template_app.runtime.container.runtime.scope_manager import ScopeManager


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
    scope_id: ScopeID) -> None:

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
    from template_app.runtime.container.exceptions import (
        ScopeRequiredError,
    )

    with pytest.raises(ScopeRequiredError):
        scope_manager.get_scope(scope_id)


def test_scopes_count(scope_manager: ScopeManager) -> None:
    first = scope_manager.create_scope()
    second = scope_manager.create_scope()

    assert scope_manager.scopes_count == 2

    scope_manager.close_scope(first)
    scope_manager.close_scope(second)

    assert scope_manager.scopes_count == 0
