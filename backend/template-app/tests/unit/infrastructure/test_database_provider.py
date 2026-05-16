from __future__ import annotations

import pytest

from template_app.infrastructure.providers.database import DatabaseProvider


@pytest.mark.asyncio
async def test_database_provider_lifecycle() -> None:
    provider = DatabaseProvider()

    assert provider.started is False

    await provider.startup()

    assert provider.started is True

    await provider.shutdown()

    assert provider.started is False
