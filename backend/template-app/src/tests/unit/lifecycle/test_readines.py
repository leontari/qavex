from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.manager import (
    LifecycleManager,
)
from template_app.runtime.lifecycle.models import (
    ReadinessProbe,
)
from template_app.runtime.lifecycle.registry import (
    LifecycleRegistry,
)


@pytest.mark.asyncio
async def test_readiness_probe_success() -> None:

    registry = LifecycleRegistry()

    async def probe() -> bool:
        return True

    registry.register_probe(
        ReadinessProbe(
            name="database",
            handler=probe,
        )
    )

    manager = LifecycleManager(
        registry=registry,
    )

    await manager.startup()

    assert manager.state.ready is True
