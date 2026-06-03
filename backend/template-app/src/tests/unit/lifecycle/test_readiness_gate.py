from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.readiness import ReadinessGate


def test_gate_is_not_ready_by_default() -> None:
    """
    Runtime must start in NOT READY state.
    """
    gate = ReadinessGate()

    assert gate.is_ready is False


def test_gate_can_be_marked_ready() -> None:
    """
    Runtime readiness must be mutable.
    """
    gate = ReadinessGate()

    gate.mark_ready()

    assert gate.is_ready is True


def test_gate_can_be_marked_not_ready() -> None:
    """
    Runtime readiness must support reset.
    """
    gate = ReadinessGate()

    gate.mark_ready()
    gate.mark_not_ready()

    assert gate.is_ready is False


def test_ensure_ready_raises_when_not_ready() -> None:
    """
    ensure_ready must protect transports
    from premature startup.
    """
    gate = ReadinessGate()

    with pytest.raises(
        RuntimeError,
        match="Runtime is not ready.",
    ):
        gate.ensure_ready()


def test_ensure_ready_passes_when_ready() -> None:
    """
    ensure_ready must pass
    after runtime becomes ready.
    """
    gate = ReadinessGate()

    gate.mark_ready()

    gate.ensure_ready()
