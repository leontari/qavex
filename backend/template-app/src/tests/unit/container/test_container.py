from __future__ import annotations

from unittest.mock import Mock, AsyncMock, MagicMock

import pytest

from template_app.runtime.container import (
    Container,
    Namespace,
    DependencyScope,
    DependencyVisibility, DependencyProvider,
)

from template_app.runtime.container.runtime.scope import ScopeHandle
from template_app.runtime.container.diagnostics import ContainerDiagnostics


class ServiceA: ...
class ServiceB: ...


def test_container_initializes_manager(container: Container) -> None:
    assert container._manager is not None


def test_diagnostics_uses_container_manager(container: Container) -> None:
    assert container.diagnostics._manager is container._manager


def test_container_initializes_diagnostics(container: Container) -> None:
    assert container.diagnostics is not None
    assert isinstance(container.diagnostics, ContainerDiagnostics)


def test_diagnostics_is_single_instance(container: Container) -> None:
    assert container.diagnostics is container.diagnostics


def test_register_delegates_to_manager(
    fake_string_provider: DependencyProvider[str],
    container: Container,
    namespace_a: Namespace,
) -> None:
    manager = Mock()
    container._manager = manager

    container.register(
        contract=str,
        provider=fake_string_provider,
        namespace=namespace_a,
        visibility=DependencyVisibility.PUBLIC,
        scope=DependencyScope.SINGLETON,
        overwrite=True,
    )

    manager.register.assert_called_once_with(
        contract=str,
        provider=fake_string_provider,
        namespace=namespace_a,
        visibility=DependencyVisibility.PUBLIC,
        scope=DependencyScope.SINGLETON,
        overwrite=True,
    )


@pytest.mark.asyncio
async def test_resolve_delegates_to_manager(
    container: Container,
    owner_namespace: Namespace,
    requester_namespace: Namespace,
) -> None:

    manager = MagicMock()
    manager.resolve = AsyncMock(return_value="service")

    container._manager = manager

    result = await container.resolve(
        str,
        namespace=owner_namespace,
        requester=requester_namespace,
    )

    assert result == "service"

    manager.resolve.assert_awaited_once_with(
        contract=str,
        namespace=owner_namespace,
        requester=requester_namespace,
    )


@pytest.mark.asyncio
async def test_resolve_forwards_requester(
    container: Container,
    owner_namespace: Namespace,
    requester_namespace: Namespace,
) -> None:

    manager = MagicMock()
    manager.resolve = AsyncMock(return_value="service")
    container._manager = manager

    result = await container.resolve(
        str,
        namespace=owner_namespace,
        requester=requester_namespace,
    )

    assert result == "service"

    manager.resolve.assert_awaited_once_with(
        contract=str,
        namespace=owner_namespace,
        requester=requester_namespace,
    )


def test_scope_returns_scope_handle(container: Container) -> None:
    handle = container.scope()

    assert isinstance(handle, ScopeHandle)


def test_scope_uses_manager_context_and_scopes(container: Container) -> None:
    handle = container.scope()

    assert handle._scopes is container._manager.scopes
    assert handle._context is container._manager.context


def test_diagnostics_returns_facade(container: Container) -> None:

    diagnostics = container.diagnostics

    assert isinstance(diagnostics, ContainerDiagnostics)


def test_scope_returns_new_handle_each_call(container: Container) -> None:
    first = container.scope()
    second = container.scope()

    assert first is not second

#############
# integration
#############

class Service:
    pass


class ServiceProvider:
    async def provide(
        self,
        resolver,
    ) -> Service:
        return Service()


@pytest.mark.asyncio
async def test_register_and_resolve_transient(
    namespace: Namespace,
    container: Container,
) -> None:
    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=namespace,
        scope=DependencyScope.TRANSIENT,
    )

    instance = await container.resolve(
        Service,
        namespace=namespace,
    )

    assert isinstance(instance, Service)


@pytest.mark.asyncio
async def test_register_and_resolve_singleton(
    namespace: Namespace,
    container: Container,
) -> None:

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=namespace,
        scope=DependencyScope.SINGLETON,
    )

    first = await container.resolve(Service, namespace=namespace)
    second = await container.resolve(Service, namespace=namespace)

    assert first is second


@pytest.mark.asyncio
async def test_register_and_resolve_scoped(
    namespace,
) -> None:
    container = Container()

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=namespace,
        scope=DependencyScope.SCOPED,
    )

    async with container.scope():

        first = await container.resolve(Service, namespace=namespace)
        second = await container.resolve(Service, namespace=namespace)

        assert first is second
