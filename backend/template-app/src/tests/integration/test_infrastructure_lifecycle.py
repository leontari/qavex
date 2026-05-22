from __future__ import annotations

import pytest

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


@pytest.mark.asyncio
async def test_infrastructure_providers_execute_lifecycle() -> None:
    kernel = bootstrap_application()

    providers = (
        kernel._context
        .runtime
        .infrastructure_registry
        .providers
    )

    await kernel.startup()

    assert all(
        provider.started
        for provider in providers
    )

    await kernel.shutdown()

    assert all(
        not provider.started
        for provider in providers
    )
