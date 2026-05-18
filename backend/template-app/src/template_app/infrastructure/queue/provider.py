from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class QueueProvider:
    """Queue provider."""

    brokers: list[str]

    started: bool = field(
        default=False,
        init=False,
    )

    @property
    def name(self) -> str:
        return "queue"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False
