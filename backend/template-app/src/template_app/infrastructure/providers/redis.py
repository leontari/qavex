from __future__ import annotations


class RedisProvider:
    """Redis infrastructure provider."""

    name = "redis"

    def __init__(self) -> None:
        self.started = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False
