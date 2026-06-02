from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel


@pytest.mark.asyncio
async def test_kernel_startup(kernel: RuntimeKernel) -> None:
    """
    Runtime kernel should start up safely.
    """
    await kernel.startup()


@pytest.mark.asyncio
async def test_kernel_shutdown(kernel: RuntimeKernel) -> None:
    """
    Runtime kernel should shut down safely.
    """
    await kernel.shutdown()
