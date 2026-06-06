from __future__ import annotations

import pytest

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    AsyncProvider,
)


class AsyncService:
    pass


@pytest.mark.asyncio
async def test_async_dependency_resolution() -> None:
    manager = DependencyManager()

    async def factory(
        _: DependencyManager,
    ) -> AsyncService:
        return AsyncService()

    manager.register(
        AsyncService,
        AsyncProvider(factory),
        namespace="kernel",
    )

    instance = await manager.resolve_async(
        AsyncService,
        namespace="kernel",
    )

    assert isinstance(
        instance,
        AsyncService,
    )


@pytest.mark.asyncio
async def test_async_provider_returns_new_instance() -> None:
    manager = DependencyManager()

    async def factory(
        _: DependencyManager,
    ) -> AsyncService:
        return AsyncService()

    manager.register(
        AsyncService,
        AsyncProvider(factory),
        namespace="kernel",
    )

    first = await manager.resolve_async(
        AsyncService,
        namespace="kernel",
    )

    second = await manager.resolve_async(
        AsyncService,
        namespace="kernel",
    )

    assert first is not second


@pytest.mark.asyncio
async def test_sync_provider_via_async_resolve() -> None:
    from template_app.runtime.container.providers import (
        SingletonProvider,
    )

    manager = DependencyManager()

    manager.register(
        AsyncService,
        SingletonProvider(
            lambda _: AsyncService(),
        ),
        namespace="kernel",
    )

    first = await manager.resolve_async(
        AsyncService,
        namespace="kernel",
    )

    second = await manager.resolve_async(
        AsyncService,
        namespace="kernel",
    )

    assert first is second


@pytest.mark.asyncio
async def test_async_resolve_preserves_namespace_isolation() -> None:
    manager = DependencyManager()

    async def factory(
        _: DependencyManager,
    ) -> AsyncService:
        return AsyncService()

    manager.register(
        AsyncService,
        AsyncProvider(factory),
        namespace="plugin.billing",
    )

    instance = await manager.resolve_async(
        AsyncService,
        namespace="plugin.billing",
    )

    assert isinstance(
        instance,
        AsyncService,
    )
