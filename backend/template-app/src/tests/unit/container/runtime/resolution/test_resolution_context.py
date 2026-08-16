from __future__ import annotations

from template_app.runtime.container.runtime.dependency import DependencyID
from template_app.runtime.container.runtime.scope import ScopeID
from template_app.runtime.container.runtime.resolution import (
    ResolutionContext,
)


def test_push_adds_dependency(dependency_id: DependencyID) -> None:
    context = ResolutionContext()
    updated = context.push(dependency_id)

    assert updated.stack == (dependency_id,)
    assert context.stack == ()


def test_push_preserves_metadata(
    dependency_id: DependencyID,
    scope_id: ScopeID,
) -> None:
    context = ResolutionContext(scope_id=scope_id)
    updated = context.push(dependency_id)

    assert updated.scope_id == scope_id


def test_pop_removes_last_dependency(dependency_id: DependencyID) -> None:
    context = ResolutionContext(stack=(dependency_id,))
    updated = context.pop()

    assert updated.stack == ()


def test_pop_empty_stack_is_safe() -> None:
    context = ResolutionContext()
    updated = context.pop()

    assert updated.stack == ()
