from __future__ import annotations

from tests.support.fakes.transports import FakeTransport


class TransportBuilder:
    """
    Runtime transport builder.

    Responsibilities:
        - transport generation
        - transport customization
        - runtime-safe transport creation
    """

    @staticmethod
    def fake(name: str = "fake") -> FakeTransport:
        """
        Build fake transport.
        """
        return FakeTransport(name=name)
