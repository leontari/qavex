from __future__ import annotations

from template_app.runtime.transports.manager import (
    TransportManager,
)
from template_app.runtime.transports.runtime import (
    TransportRuntime,
)


def test_transport_runtime_exposes_manager() -> None:
    """
    Transport runtime should expose manager.
    """
    manager = TransportManager()

    runtime = TransportRuntime(
        manager=manager,
    )

    assert runtime.manager is manager
