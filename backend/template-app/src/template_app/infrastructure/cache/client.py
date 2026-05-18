"""Provider Example."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CacheClient:
    """Cache client."""

    url: str

    async def ping(self) -> bool:
        return True
