from template_app.runtime.runtime.graph.validator import (
    RuntimeGraphValidator,
)
from tests.factories.runtime import build_runtime_state


def test_runtime_graph_validates() -> None:
    runtime = build_runtime_state()

    RuntimeGraphValidator.validate(runtime)
