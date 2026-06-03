from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.graph.validator import (
    RuntimeGraphValidator,
)


def test_runtime_graph_validates(kernel: RuntimeKernel) -> None:
    runtime_graph = kernel.runtime

    RuntimeGraphValidator.validate(runtime_graph)
