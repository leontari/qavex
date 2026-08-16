import pytest

from template_app.runtime.container.exceptions import DependencyCycleError
from template_app.runtime.container.runtime.dependency import DependencyID
from template_app.runtime.container.runtime.scope import ScopeID
from template_app.runtime.container.runtime.resolution import (
    ResolutionManager,
)
from tests.plugins.container import context_manager


def test_current_returns_default_context(
    context_manager: ResolutionManager
) -> None:
    assert context_manager.current_context.scope_id is None
    assert context_manager.current_context.stack == ()


def test_enter_scope_updates_context(
    scope_id: ScopeID,
    context_manager: ResolutionManager
) -> None:
    token = context_manager.enter_scope(scope_id)

    try:
        assert context_manager.current_context.scope_id == scope_id
    finally:
        context_manager.leave_scope(token)


def test_leave_scope_restores_context(
    scope_id: ScopeID,
    context_manager: ResolutionManager
) -> None:
    token = context_manager.enter_scope(scope_id)
    context_manager.leave_scope(token)

    assert context_manager.current_context.scope_id is None


def test_enter_resolution_pushes_dependency(
    dependency_id: DependencyID,
    context_manager: ResolutionManager,
) -> None:
    token = context_manager.enter_resolution(dependency_id)

    try:
        assert context_manager.current_context.stack == (dependency_id,)
    finally:
        context_manager.leave_resolution(token)


def test_leave_resolution_restores_stack(
    dependency_id: DependencyID,
    context_manager: ResolutionManager,
) -> None:
    token = context_manager.enter_resolution(dependency_id)
    context_manager.leave_resolution(token)

    assert context_manager.current_context.stack == ()


def test_cycle_detection(
    dependency_id: DependencyID,
    context_manager: ResolutionManager,
) -> None:
    token = context_manager.enter_resolution(dependency_id)

    try:
        with pytest.raises(DependencyCycleError):
            context_manager.enter_resolution(dependency_id)
    finally:
        context_manager.leave_resolution(token)


def test_current_scope_property(
    scope_id: ScopeID,
    context_manager: ResolutionManager,
) -> None:
    token = context_manager.enter_scope(scope_id)

    try:
        assert context_manager.current_context.scope_id == scope_id
    finally:
        context_manager.leave_scope(token)


def test_enter_scope_updates_current_context(
    context_manager: ResolutionManager,
    scope_id: ScopeID,
) -> None:
    token = context_manager.enter_scope(scope_id)

    try:
        assert context_manager.current_context.scope_id == scope_id
    finally:
        context_manager.leave_scope(token)


def test_leave_scope_restores_previous_context(
    context_manager: ResolutionManager,
    scope_id: ScopeID,
) -> None:
    previous = context_manager.current_context
    token = context_manager.enter_scope(scope_id)
    context_manager.leave_scope(token)

    assert context_manager.current_context == previous


def test_cycle_chain_property(
    dependency_a: DependencyID,
    dependency_b: DependencyID,
) -> None:
    error = DependencyCycleError(
        (dependency_a, dependency_b),
        dependency_a,
    )

    expected = (
        f"{dependency_a}"
        f" -> {dependency_b}"
        f" -> {dependency_a}"
    )

    assert error.chain == expected


def test_cycle_length(
    dependency_a: DependencyID,
    dependency_b: DependencyID,
) -> None:
    error = DependencyCycleError(
        (dependency_a, dependency_b),
        dependency_a,
    )

    assert error.cycle_length == 3


def test_cycle_message(
    dependency_a: DependencyID,
    dependency_b: DependencyID,
) -> None:
    error = DependencyCycleError(
        (dependency_a, dependency_b),
        dependency_a,
    )

    assert str(error).startswith("Circular dependency detected:")
