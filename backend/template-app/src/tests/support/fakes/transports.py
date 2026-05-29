from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FakeTransport:
    """
    Runtime fake transport.
    """

    name: str = "fake"

    started: bool = False

    stopped: bool = False

    events: list[str] = field(default_factory=list)

    async def startup(self) -> None:
        self.started = True

        self.events.append(f"startup:{self.name}")

    async def shutdown(self) -> None:
        self.stopped = True

        self.events.append(f"shutdown:{self.name}")


class FakeHttpTransport(FakeTransport):
    pass


class FakeKafkaTransport(FakeTransport):
    pass
