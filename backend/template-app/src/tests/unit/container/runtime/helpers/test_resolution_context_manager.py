import pytest

from template_app.runtime.container.exceptions import DependencyCycleError
from template_app.runtime.container.runtime.helpers.context_manager import (
    ResolutionContextManager,
)


def test_current_returns_default_context():
    manager = ResolutionContextManager()

    assert manager.current.scope_id is None
    assert manager.current.stack == ()


def test_enter_scope_updates_context(scope_id):
    manager = ResolutionContextManager()
    token = manager.enter_scope(scope_id)

    try:
        assert manager.current.scope_id == scope_id
    finally:
        manager.leave_scope(token)


def test_leave_scope_restores_context(scope_id):
    manager = ResolutionContextManager()
    token = manager.enter_scope(scope_id)
    manager.leave_scope(token)

    assert manager.current.scope_id is None


def test_enter_resolution_pushes_dependency(dependency_id):
    manager = ResolutionContextManager()
    token = manager.enter_resolution(dependency_id)

    try:
        assert manager.current.stack == (dependency_id,)
    finally:
        manager.leave_resolution(token)


def test_leave_resolution_restores_stack(dependency_id):
    manager = ResolutionContextManager()
    token = manager.enter_resolution(dependency_id)

    manager.leave_resolution(token)

    assert manager.current.stack == ()


def test_cycle_detection(dependency_id):
    manager = ResolutionContextManager()
    token = manager.enter_resolution(dependency_id)

    try:
        with pytest.raises(DependencyCycleError):
            manager.enter_resolution(dependency_id)
    finally:
        manager.leave_resolution(token)


def test_current_scope_property(scope_id):
    manager = ResolutionContextManager()
    token = manager.enter_scope(scope_id)

    try:
        assert manager.current_scope == scope_id
    finally:
        manager.leave_scope(token)
