from __future__ import annotations

import pytest

from template_app.infrastructure.database import DatabaseProvider


@pytest.mark.asyncio
async def test_database_provider_lifecycle() -> None:
    provider = DatabaseProvider(
        dsn="postgresql://localhost/test",
    )

    assert not provider.started

    await provider.startup()

    assert provider.started

    await provider.shutdown()

    assert not provider.started
