from __future__ import annotations

import pytest

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


@pytest.mark.asyncio
async def test_kernel_executes_lifecycle() -> None:
    kernel = bootstrap_application()

    await kernel.startup()
    await kernel.shutdown()
