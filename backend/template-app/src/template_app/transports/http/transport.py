from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI


@dataclass(slots=True)
class FastAPITransport:
    app: FastAPI

    async def startup(self) -> None:
        return None

    async def shutdown(self) -> None:
        return None
