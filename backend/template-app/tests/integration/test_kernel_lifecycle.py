from __future__ import annotations

import pytest

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

@pytest.mark.asyncio
async def test_kernel_startup_executes_hooks() -> None:
    kernel = bootstrap_application()

    hooks = (
        kernel.context
        .runtime
        .lifecycle_registry
        .startup_hooks
    )

    assert len(hooks) > 0

    await kernel.startup()
    # if no exception -> success
