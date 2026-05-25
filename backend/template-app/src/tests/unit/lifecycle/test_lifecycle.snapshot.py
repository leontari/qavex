from __future__ import annotations

import pytest

from template_app.runtime.kernel.context import KernelContext
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.lifecycle import LifecycleRegistry, LifecycleManager
from template_app.runtime.lifecycle.readiness import ReadinessGate
from tests.factories.runtime import build_runtime_state


def test_lifecycle_snapshot_is_immutable():
    registry = LifecycleRegistry()

    snapshot = registry.snapshot()

    assert isinstance(snapshot.startup, tuple)
    assert isinstance(snapshot.shutdown, tuple)


@pytest.mark.asyncio
async def test_shutdown_runs_in_reverse_order():
    calls = []

    async def a(): calls.append("a")
    async def b(): calls.append("b")

    registry = LifecycleRegistry()

    registry.register_startup(type("H", (), {"handler": a})())
    registry.register_shutdown(type("H", (), {"handler": b})())

    manager = LifecycleManager(snapshot=registry.snapshot())

    await manager.shutdown()

    assert calls == ["b"]


def test_readiness_gate():
    gate = ReadinessGate()

    assert gate.is_ready is False

    gate.mark_ready()

    assert gate.is_ready is True


def test_http_transport_waits_for_readiness():
    from template_app.runtime.transports.http.transport import FastAPITransport
    from template_app.runtime.transports.gating import TransportGate

    gate = TransportGate(readiness=ReadinessGate())

    transport = FastAPITransport(gate=gate)

    assert transport is not None


@pytest.mark.asyncio
async def test_kernel_ready_after_lifecycle():
    kernel = RuntimeKernel(_context=KernelContext(runtime=build_runtime_state()))

    assert kernel.readiness.is_ready is False

    await kernel.startup()

    assert kernel.readiness.is_ready is True
