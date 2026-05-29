from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_kernel_startup(
    kernel_harness,
) -> None:
    """
    Runtime kernel should start up safely.
    """
    await kernel_harness.startup()


@pytest.mark.asyncio
async def test_kernel_shutdown(
    kernel_harness,
) -> None:
    """
    Runtime kernel should shut down safely.
    """
    await kernel_harness.shutdown()
