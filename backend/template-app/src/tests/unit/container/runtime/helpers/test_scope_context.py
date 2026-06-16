import asyncio


def test_contains_false(scope_context, dependency_id):
    assert not scope_context.contains(dependency_id)


def test_set_and_get_instance(scope_context, dependency_id):
    instance = object()
    scope_context.set(dependency_id, instance)

    assert scope_context.contains(dependency_id)
    assert scope_context.get(dependency_id) is instance


def test_get_missing_raises(scope_context, dependency_id):
    import pytest

    with pytest.raises(KeyError):
        scope_context.get(dependency_id)


def test_future_lifecycle(scope_context, dependency_id):
    future = asyncio.Future()
    scope_context.set_future(dependency_id, future)

    assert scope_context.get_future(dependency_id) is future

    scope_context.remove_future(dependency_id)

    assert scope_context.get_future(dependency_id) is None


def test_clear_removes_everything(scope_context, dependency_id):
    scope_context.set(dependency_id, object())
    scope_context.set_future(dependency_id, asyncio.Future())
    scope_context.clear()

    assert not scope_context.instances
    assert scope_context.get_future(dependency_id) is None
