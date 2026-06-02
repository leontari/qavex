from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.graph.inspector import (
    RuntimeGraphInspector,
)


def test_runtime_inspector_returns_snapshot(kernel: RuntimeKernel) -> None:
    snapshot = RuntimeGraphInspector.inspect(kernel.runtime)

    assert "modules" in snapshot
