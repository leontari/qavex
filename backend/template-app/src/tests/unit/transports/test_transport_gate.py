from __future__ import annotations

from template_app.runtime.lifecycle.readiness import (
    ReadinessGate,
)
from template_app.runtime.transports.gating import (
    TransportGate,
)


def test_transport_gate_allows_ready_runtime() -> None:
    """
    Transport gate should allow startup
    when runtime ready.
    """
    readiness = ReadinessGate()

    readiness.mark_ready()

    gate = TransportGate(
        readiness=readiness,
    )

    assert gate.allow_start() is True


def test_transport_gate_blocks_unready_runtime() -> None:
    """
    Transport gate should block startup
    when runtime not ready.
    """
    readiness = ReadinessGate()

    gate = TransportGate(
        readiness=readiness,
    )

    assert gate.allow_start() is False
