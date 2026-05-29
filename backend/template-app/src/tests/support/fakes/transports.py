from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FakeTransport:
    """
    Runtime-safe fake transport.

    Responsibilities:
        - transport contract testing
        - lifecycle orchestration testing
        - startup/shutdown verification

    Notes:
        Must NEVE depend on:
            - FastAPI
            - Kafka
            - gRPC
            - uvicorn
            - external runtime
    """

    name: str = "fake"

    started: bool = field(default=False, init=False)
    stopped: bool = field(default=False, init=False)

    startup_calls: int = field(default=0, init=False)
    shutdown_calls: int = field(default=0, init=False)

    events: list[str] = field(default_factory=list)

    async def startup(self) -> None:
        self.started = True
        self.startup_calls += 1
        self.events.append(f"startup:{self.name}")

    async def shutdown(self) -> None:
        self.stopped = True
        self.shutdown_calls += 1
        self.events.append(f"shutdown:{self.name}")


class FakeHttpTransport(FakeTransport):
    pass


class FakeKafkaTransport(FakeTransport):
    pass
