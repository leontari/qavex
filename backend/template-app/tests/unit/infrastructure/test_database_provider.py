from __future__ import annotations

import pytest

from template_app.infrastructure.database import DatabaseProvider


@pytest.mark.asyncio
async def test_database_provider_lifecycle() -> None:
    provider = DatabaseProvider(
        dsn="postgresql://localhost/test",
    )

    assert provider.started is False

    await provider.startup()

    assert provider.started is True

    await provider.shutdown()

    assert provider.started is False
