from __future__ import annotations

import pytest

from template_app.runtime.kernel.bootstrap import bootstrap_kernel


@pytest.mark.asyncio
async def test_kernel_executes_lifecycle() -> None:
    kernel = bootstrap_kernel()

    await kernel.startup()
    await kernel.shutdown()
