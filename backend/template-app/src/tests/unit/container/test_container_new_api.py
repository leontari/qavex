from unittest.mock import AsyncMock

import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models import Namespace

# 1. Container передает requester в manager
@pytest.mark.asyncio
async def test_resolve_passes_requester_to_manager() -> None:
    container = Container()

    manager = AsyncMock()
    container._manager = manager

    owner = Namespace("kernel")
    requester = Namespace("plugin.auth")

    await container.resolve(
        object,
        namespace=owner,
        requester=requester,
    )

    manager.resolve.assert_awaited_once_with(
        contract=object,
        namespace=owner,
        requester=requester,
    )


# 2. register продолжает работать
def test_register_passes_namespace_to_manager() -> None:
    container = Container()

    namespace = Namespace("kernel")

    manager = Mock()
    container._manager = manager

    provider = Mock()

    container.register(
        contract=object,
        provider=provider,
        namespace=namespace,
    )

    manager.register.assert_called_once()

# 3. register + resolve integration
import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models import Namespace


class Service:
    pass


class ServiceProvider:
    async def provide(self, resolver):
        return Service()


@pytest.mark.asyncio
async def test_register_and_resolve() -> None:
    container = Container()

    owner = Namespace("kernel")

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner,
    )

    instance = await container.resolve(
        Service,
        namespace=owner,
        requester=owner,
    )

    assert isinstance(instance, Service)


# 4. requester не влияет на PUBLIC
@pytest.mark.asyncio
async def test_public_dependency_resolves_from_foreign_namespace():
    container = Container()

    owner = Namespace("kernel")
    requester = Namespace("plugin.auth")

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner,
    )

    instance = await container.resolve(
        Service,
        namespace=owner,
        requester=requester,
    )

    assert isinstance(instance, Service)

# 5. PRIVATE visibility blocks foreign requester
import pytest

from template_app.runtime.container.exceptions import (
    VisibilityViolationError,
)
from template_app.runtime.container.models import (
    DependencyVisibility,
)


@pytest.mark.asyncio
async def test_private_dependency_blocks_foreign_requester():
    container = Container()

    owner = Namespace("plugin.auth")
    requester = Namespace("plugin.billing")

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner,
        visibility=DependencyVisibility.PRIVATE,
    )

    with pytest.raises(VisibilityViolationError):
        await container.resolve(
            Service,
            namespace=owner,
            requester=requester,
        )


# 6. PRIVATE visibility allows owner
@pytest.mark.asyncio
async def test_private_dependency_allows_owner():
    container = Container()

    owner = Namespace("plugin.auth")

    container.register(
        contract=Service,
        provider=ServiceProvider(),
        namespace=owner,
        visibility=DependencyVisibility.PRIVATE,
    )

    instance = await container.resolve(
        Service,
        namespace=owner,
        requester=owner,
    )

    assert isinstance(instance, Service)


# 7. requester обязателен если убраны дефолтные значения
import pytest


@pytest.mark.asyncio
async def test_resolve_requires_requester(
    container: Container,
):
    with pytest.raises(TypeError):
        await container.resolve(
            Service,
            namespace=Namespace("kernel"),
        )

# Дополнительно для DependencyManager
# Если сейчас
# DependencyManager.resolve(
#     contract,
#     namespace,
#     requester,
# )
@pytest.mark.asyncio
async def test_manager_forwards_requester_to_internal_resolve(
    manager: DependencyManager,
):
    manager._resolve_dependency = AsyncMock()

    owner = Namespace("kernel")
    requester = Namespace("plugin.auth")

    await manager.resolve(
        contract=Service,
        namespace=owner,
        requester=requester,
    )

    manager._resolve_dependency.assert_awaited_once()

    _, kwargs = manager._resolve_dependency.await_args

    assert kwargs["requester"] == requester
