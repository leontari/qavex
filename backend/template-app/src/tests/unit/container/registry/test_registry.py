"""Tests for DependencyRegistry."""

from __future__ import annotations

import pytest

from template_app.runtime.container.exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)
from template_app.runtime.container.models.dependency import (
    DependencyDescriptor,
    DependencyID,
)
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import DependencyScope
from template_app.runtime.container.models.visibility import DependencyVisibility
from template_app.runtime.container.providers import FactoryProvider
from template_app.runtime.container.runtime.registry import DependencyRegistry


class ServiceA: ...


class ServiceB: ...


@pytest.fixture
def registry() -> DependencyRegistry:
    return DependencyRegistry()


@pytest.fixture
def namespace() -> Namespace:
    return Namespace(name="test")


@pytest.fixture
def dependency_id(namespace: Namespace) -> DependencyID:
    return DependencyID(
        namespace=namespace,
        contract=ServiceA,
    )


@pytest.fixture
def descriptor(
    dependency_id: DependencyID,
) -> DependencyDescriptor:
    return DependencyDescriptor(
        ident=dependency_id,
        provider=FactoryProvider(ServiceA),
        scope=DependencyScope.TRANSIENT,
        visibility=DependencyVisibility.PUBLIC,
    )


def test_add_descriptor(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    assert registry.contains(descriptor.ident)


def test_add_duplicate_raises(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    with pytest.raises(
        DependencyAlreadyRegisteredError,
    ):
        registry.add(descriptor)


def test_replace_descriptor(
    registry: DependencyRegistry,
    dependency_id: DependencyID,
) -> None:
    descriptor_a = DependencyDescriptor(
        ident=dependency_id,
        provider=FactoryProvider(ServiceA),
        scope=DependencyScope.TRANSIENT,
        visibility=DependencyVisibility.PUBLIC,
    )

    descriptor_b = DependencyDescriptor(
        ident=dependency_id,
        provider=FactoryProvider(ServiceB),
        scope=DependencyScope.TRANSIENT,
        visibility=DependencyVisibility.PUBLIC,
    )

    registry.add(descriptor_a)
    registry.replace(descriptor_b)

    assert registry.get(
        dependency_id,
    ) is descriptor_b


def test_replace_missing_raises(
    registry: DependencyRegistry,
    dependency_id: DependencyID,
) -> None:
    descriptor = DependencyDescriptor(
        ident=dependency_id,
        provider=FactoryProvider(ServiceA),
        scope=DependencyScope.TRANSIENT,
        visibility=DependencyVisibility.PUBLIC,
    )

    with pytest.raises(
        DependencyNotFoundError,
    ):
        registry.replace(descriptor)


def test_get_descriptor(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    result = registry.get(
        descriptor.ident,
    )

    assert result is descriptor


def test_get_missing_raises(
    registry: DependencyRegistry,
    dependency_id: DependencyID,
) -> None:
    with pytest.raises(
        DependencyNotFoundError,
    ):
        registry.get(dependency_id)


def test_remove_descriptor(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    removed = registry.remove(
        descriptor.ident,
    )

    assert removed is descriptor
    assert not registry.contains(
        descriptor.ident,
    )


def test_remove_missing_raises(
    registry: DependencyRegistry,
    dependency_id: DependencyID,
) -> None:
    with pytest.raises(
        DependencyNotFoundError,
    ):
        registry.remove(dependency_id)


def test_contains(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    assert not registry.contains(
        descriptor.ident,
    )

    registry.add(descriptor)

    assert registry.contains(
        descriptor.ident,
    )


def test_clear(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    registry.clear()

    assert registry.size == 0
    assert registry.descriptors == ()


def test_namespaces(
    registry: DependencyRegistry,
    namespace: Namespace,
) -> None:
    dependency_a = DependencyID(
        namespace=namespace,
        contract=ServiceA,
    )

    dependency_b = DependencyID(
        namespace=namespace,
        contract=ServiceB,
    )

    registry.add(
        DependencyDescriptor(
            ident=dependency_a,
            provider=FactoryProvider(ServiceA),
            scope=DependencyScope.TRANSIENT,
            visibility=DependencyVisibility.PUBLIC,
        ),
    )

    registry.add(
        DependencyDescriptor(
            ident=dependency_b,
            provider=FactoryProvider(ServiceB),
            scope=DependencyScope.TRANSIENT,
            visibility=DependencyVisibility.PUBLIC,
        ),
    )

    assert registry.namespaces == frozenset(
        {namespace},
    )


def test_descriptors_snapshot_is_immutable(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    snapshot = registry.descriptors

    registry.clear()

    assert len(snapshot) == 1
    assert snapshot[0] is descriptor


def test_dependency_ids_snapshot_is_immutable(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    snapshot = registry.dependency_ids

    registry.clear()

    assert len(snapshot) == 1
    assert snapshot[0] == descriptor.ident


def test_items(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    registry.add(descriptor)

    items = registry.items()

    assert len(items) == 1

    dependency_id, stored = items[0]

    assert dependency_id == descriptor.ident
    assert stored is descriptor


def test_size(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    assert registry.size == 0

    registry.add(descriptor)

    assert registry.size == 1


def test_is_empty(
    registry: DependencyRegistry,
    descriptor: DependencyDescriptor,
) -> None:
    assert registry.is_empty is True

    registry.add(descriptor)

    assert registry.is_empty is False
