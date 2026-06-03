from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel


@pytest.mark.asyncio
async def test_kernel_lifecycle_executes(kernel: RuntimeKernel) -> None:
    await kernel.startup()
    await kernel.shutdown()
