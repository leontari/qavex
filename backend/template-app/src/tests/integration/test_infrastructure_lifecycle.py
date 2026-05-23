from __future__ import annotations

import pytest

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


@pytest.mark.asyncio
async def test_infrastructure_providers_execute_lifecycle() -> None:
    kernel = bootstrap_kernel()

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
