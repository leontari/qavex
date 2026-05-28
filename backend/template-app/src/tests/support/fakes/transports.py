from dataclasses import dataclass

from template_app.runtime.transports.contracts import Transport


@dataclass
class FakeTransport(Transport):

    started: bool = False
    stopped: bool = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.stopped = True


class FakeHttpTransport(FakeTransport):
    pass


class FakeKafkaTransport(FakeTransport):
    pass
