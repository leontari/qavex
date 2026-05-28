from __future__ import annotations

import pytest

from tests.support.factories.kernel import (
    build_testing_kernel,
)


@pytest.mark.asyncio
async def test_kernel_startup_executes_hooks() -> None:
    kernel = build_testing_kernel()

    runtime_module = next(
        manifest.module
        for manifest in kernel.modules
        if manifest.name == "runtime"
    )

    assert runtime_module.started is False

    await kernel.startup()

    assert runtime_module.started is True


@pytest.mark.asyncio
async def test_kernel_shutdown_executes_hooks() -> None:
    kernel = build_testing_kernel()

    runtime_module = next(
        manifest.module
        for manifest in kernel.modules
        if manifest.name == "runtime"
    )

    await kernel.startup()

    assert runtime_module.started is True

    await kernel.shutdown()

    assert runtime_module.started is False
