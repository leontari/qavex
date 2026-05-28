from __future__ import annotations

import pytest

from template_app.runtime.infrastructure.infra import CacheProvider


@pytest.mark.asyncio
async def test_cache_provider_startup() -> None:
    provider = CacheProvider(
        url="redis://localhost",
    )

    await provider.startup()

    assert provider.started is True
    assert provider.client is not None


@pytest.mark.asyncio
async def test_cache_provider_shutdown() -> None:
    provider = CacheProvider(
        url="redis://localhost",
    )

    await provider.startup()
    await provider.shutdown()

    assert provider.started is False


@pytest.mark.asyncio
async def test_redis_provider_lifecycle() -> None:
    provider = CacheProvider(
        url="redis://localhost",
    )

    assert provider.started is False

    await provider.startup()

    assert provider.started is True

    await provider.shutdown()

    assert provider.started is False
