from template_app.runtime.kernel.runtime.graph.inspector import (
    RuntimeGraphInspector,
)
from tests.factories.runtime import build_runtime_state


def test_runtime_inspector_returns_snapshot() -> None:
    runtime = build_runtime_state()

    snapshot = RuntimeGraphInspector.inspect(runtime)

    assert "modules" in snapshot
