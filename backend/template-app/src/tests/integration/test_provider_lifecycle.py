from __future__ import annotations

from dataclasses import dataclass

import pytest

from template_app.runtime.lifecycle import LifecycleHook
from template_app.runtime.kernel import RuntimeKernel
from template_app.runtime.kernel.bootstrap import bootstrap_kernel


@dataclass(slots=True)
class FakeInfrastructureProvider:
    """Fake infrastructure provider."""

    started: bool = False

    @property
    def name(self) -> str:
        return "fake"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False


@pytest.mark.asyncio
async def test_providers_execute_lifecycle() -> None:
    kernel: RuntimeKernel = bootstrap_kernel()

    provider = FakeInfrastructureProvider()

    runtime = kernel._context.runtime

    runtime.infrastructure_registry.register(provider)

    runtime.lifecycle_registry.register_startup(
        LifecycleHook(
            name="fake.startup",
            handler=provider.startup,
        )
    )

    runtime.lifecycle_registry.register_shutdown(
        LifecycleHook(
            name="fake.shutdown",
            handler=provider.shutdown,
        )
    )

    assert provider.started is False

    await kernel.startup()

    assert provider.started is True

    await kernel.shutdown()

    assert provider.started is False
