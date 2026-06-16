from __future__ import annotations

from dataclasses import replace

from template_app.runtime.container.runtime.helpers.resolution import (
    ResolutionContext,
)


def test_push_adds_dependency(dependency_id):
    context = ResolutionContext()
    updated = context.push(dependency_id)

    assert updated.stack == (dependency_id,)
    assert context.stack == ()


def test_push_preserves_metadata(dependency_id, scope_id):
    context = ResolutionContext(
        scope_id=scope_id,
        plugin_id="plugin",
        actor_id="actor",
        request_id="request",
    )

    updated = context.push(dependency_id)

    assert updated.scope_id == scope_id
    assert updated.plugin_id == "plugin"
    assert updated.actor_id == "actor"
    assert updated.request_id == "request"


def test_pop_removes_last_dependency(dependency_id):
    context = ResolutionContext(stack=(dependency_id,))
    updated = context.pop()

    assert updated.stack == ()


def test_pop_empty_stack_is_safe():
    context = ResolutionContext()
    updated = context.pop()

    assert updated.stack == ()


def test_with_scope_replaces_scope(scope_id):
    context = ResolutionContext()
    updated = context.with_scope(scope_id)

    assert updated.scope_id == scope_id
    assert context.scope_id is None
