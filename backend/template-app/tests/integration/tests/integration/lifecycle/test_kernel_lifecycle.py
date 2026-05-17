from __future__ import annotations

import pytest

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


@pytest.mark.asyncio
async def test_kernel_startup_executes_hooks() -> None:
    kernel = bootstrap_application()

    await kernel.startup()

    runtime_module = next(
        module
        for module in kernel.context.runtime.modules
        if module.__class__.__name__ == "RuntimeModule"
    )

    assert runtime_module.started is True


@pytest.mark.asyncio
async def test_kernel_shutdown_executes_hooks() -> None:
    kernel = bootstrap_application()

    await kernel.startup()
    await kernel.shutdown()

    runtime_module = next(
        module
        for module in kernel.context.runtime.modules
        if module.__class__.__name__ == "RuntimeModule"
    )

    assert runtime_module.stopped is True
