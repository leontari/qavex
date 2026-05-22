from __future__ import annotations

import pytest

from tests.fakes.modules import (
    FakeRuntimeModule,
)
from tests.factories.kernel import (
    build_testing_kernel,
)
from tests.factories.module_context import (
    build_module_context,
)


@pytest.mark.asyncio
async def test_kernel_startup_executes_hooks() -> None:

    kernel = build_testing_kernel()

    module = FakeRuntimeModule()

    module.setup(
        build_module_context(),
    )

    assert module.started is False

    await kernel.startup()

    assert module.started is True


@pytest.mark.asyncio
async def test_kernel_shutdown_executes_hooks() -> None:

    kernel = build_testing_kernel()

    module = FakeRuntimeModule()

    module.setup(
        build_module_context(),
    )

    await kernel.startup()

    assert module.started is True

    await kernel.shutdown()

    assert module.started is False
