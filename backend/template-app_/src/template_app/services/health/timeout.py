"""
Timeout protection utilities.

Timeout wrapper (production safety)
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


async def run_with_timeout(
    check: Callable[[], Awaitable[bool]],
    timeout: float = 2.0,
) -> bool:
    """
    Execute health check with timeout protection.

    Args:
        check:
            Async health check function.

        timeout:
            Timeout in seconds.

    Returns:
        Health check result.
    """
    try:
        return await asyncio.wait_for(check(), timeout=timeout)

    except Exception:
        return False
