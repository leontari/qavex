from __future__ import annotations

import pytest

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    AsyncProvider,
    FactoryProvider,
    SingletonProvider,
)


class Service:
    pass


def test_singleton_provider() -> None:
    provider = SingletonProvider(
        lambda _: Service(),
    )

    instance = provider.provide(
        DependencyManager(),
    )

    assert isinstance(
        instance,
        Service,
    )


def test_factory_provider() -> None:
    provider = FactoryProvider(
        lambda _: Service(),
    )

    instance = provider.provide(
        DependencyManager(),
    )

    assert isinstance(
        instance,
        Service,
    )


@pytest.mark.asyncio
async def test_async_provider() -> None:
    async def factory(
        _: DependencyManager,
    ) -> Service:
        return Service()

    provider = AsyncProvider(
        factory,
    )

    instance = await provider.provide(
        DependencyManager(),
    )

    assert isinstance(
        instance,
        Service,
    )
