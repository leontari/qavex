from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Transport(Protocol):
    async def startup(self) -> None: ...

    async def shutdown(self) -> None: ...
