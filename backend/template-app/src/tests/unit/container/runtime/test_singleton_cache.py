"""Tests for SingletonCache."""

from __future__ import annotations

import asyncio
from types import MappingProxyType

from template_app.runtime.container.models.dependency import (
    DependencyID,
)
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.runtime.singleton_cache import (
    SingletonCache,
)


class ServiceA: ...
class ServiceB: ...


def make_dependency(contract: type) -> DependencyID:
    return DependencyID(
        namespace=Namespace("test"),
        contract=contract,
    )


def test_contains_returns_false_for_unknown_dependency() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)

    assert not cache.contains(dependency)


def test_set_and_get_instance() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    instance = object()
    cache.set(dependency, instance)

    assert cache.contains(dependency)
    assert cache.get(dependency) is instance


def test_remove_instance() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    cache.set(dependency, object())
    cache.remove(dependency)

    assert not cache.contains(dependency)


def test_remove_unknown_instance_is_safe() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    cache.remove(dependency)

    assert cache.count == 0


def test_get_unknown_instance_raises_key_error() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)

    try:
        cache.get(dependency)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")


def test_count() -> None:
    cache = SingletonCache()

    cache.set(make_dependency(ServiceA), object())
    cache.set(make_dependency(ServiceB), object())

    assert cache.count == 2


def test_set_and_get_future() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    future = asyncio.Future()

    cache.set_future(dependency, future)

    assert cache.contains_future(dependency)
    assert cache.get_future(dependency) is future


def test_remove_future() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    future = asyncio.Future()

    cache.set_future(dependency, future)
    cache.remove_future(dependency)

    assert not cache.contains_future(dependency)
    assert cache.future_count == 0


def test_remove_unknown_future_is_safe() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)
    cache.remove_future(dependency)

    assert cache.future_count == 0


def test_future_count() -> None:
    cache = SingletonCache()

    cache.set_future(make_dependency(ServiceA), asyncio.Future())
    cache.set_future(make_dependency(ServiceB), asyncio.Future())

    assert cache.future_count == 2


def test_clear_removes_instances_and_futures() -> None:
    cache = SingletonCache()

    cache.set(make_dependency(ServiceA), object())
    cache.set_future(make_dependency(ServiceB), asyncio.Future())
    cache.clear()

    assert cache.count == 0
    assert cache.future_count == 0


def test_instances_returns_immutable_mapping() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)

    cache.set(dependency, object())

    instances = cache.instances

    assert isinstance(instances, MappingProxyType)

    try:
        instances[dependency] = object()
    except TypeError:
        pass
    else:
        raise AssertionError("Instances mapping must be immutable")


def test_overwrite_instance() -> None:
    cache = SingletonCache()
    dependency = make_dependency(ServiceA)

    first = object()
    second = object()

    cache.set(dependency, first)
    cache.set(dependency, second)

    assert cache.get(dependency) is second


def test_overwrite_future() -> None:
    cache = SingletonCache()

    dependency = make_dependency(ServiceA)

    first = asyncio.Future()
    second = asyncio.Future()

    cache.set_future(dependency, first)
    cache.set_future(dependency, second)

    assert cache.get_future(dependency) is second
