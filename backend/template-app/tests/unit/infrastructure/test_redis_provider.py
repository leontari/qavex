from __future__ import annotations

import pytest

from template_app.infrastructure.providers.redis import RedisProvider


@pytest.mark.asyncio
async def test_redis_provider_lifecycle() -> None:
    provider = RedisProvider()

    assert provider.started is False

    await provider.startup()

    assert provider.started is True

    await provider.shutdown()

    assert provider.started is False
