from __future__ import annotations

import pytest

from template_app.runtime.container import (
    Container,
    DependencyScope,
    Namespace,
    DependencyResolver,
)


class Service:
    pass


class ServiceProvider:
    async def provide(self, resolver: DependencyResolver) -> Service:
        return Service()


@pytest.mark.asyncio
async def test_register_and_resolve_transient(
    container: Container,
    owner_namespace: Namespace,
) -> None:
    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner_namespace,
        scope=DependencyScope.TRANSIENT,
    )

    instance1 = await container.resolve(
        Service,
        namespace=owner_namespace,
        requester=owner_namespace,
    )

    instance2 = await container.resolve(
        Service,
        namespace=owner_namespace,
        requester=owner_namespace,
    )

    assert isinstance(instance1, Service)
    assert isinstance(instance2, Service)

    assert instance1 is not instance2


@pytest.mark.asyncio
async def test_register_and_resolve_singleton(
    container: Container,
    owner_namespace: Namespace,
    requester_namespace: Namespace,
) -> None:
    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner_namespace,
        scope=DependencyScope.SINGLETON,
    )

    first = await container.resolve(
        Service,
        namespace=owner_namespace,
        requester=requester_namespace,
    )

    second = await container.resolve(
        Service,
        namespace=owner_namespace,
        requester=requester_namespace,
    )

    assert first is second


@pytest.mark.asyncio
async def test_register_and_resolve_scoped(
    container: Container,
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

        first = await container.resolve(
            Service,
            namespace=namespace,
        )

        second = await container.resolve(
            Service,
            namespace=namespace,
        )

        assert first is second

#
# @pytest.mark.asyncio
# async def test_scoped_isolation_between_scopes(
#     namespace,
# ) -> None:
#     container = Container()
#
#     container.register(
#         contract=Service,
#         provider=ServiceProvider(),
#         namespace=namespace,
#         scope=DependencyScope.SCOPED,
#     )
#
#     async with container.scope():
#         first = await container.resolve(
#             Service,
#             namespace=namespace,
#         )
#
#     async with container.scope():
#         second = await container.resolve(
#             Service,
#             namespace=namespace,
#         )
#
#     assert first is not second
#
#
# class Repository:
#     pass
#
#
# class RepositoryProvider:
#     async def provide(self, resolver) -> Repository:
#         return Repository()
#
#
# class Service:
#     def __init__(self, repository: Repository) -> None:
#         self.repository = repository
#
#
# class ServiceProvider:
#     async def provide(self, resolver) -> Service:
#         repository = await resolver.resolve(
#             Repository,
#             namespace=NAMESPACE,
#         )
#
#         return Service(repository)
#
# assert isinstance(service.repository, Repository)
