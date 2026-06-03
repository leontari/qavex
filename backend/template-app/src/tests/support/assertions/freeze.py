from template_app.runtime.kernel.kernel import RuntimeKernel


def assert_graph_frozen(kernel: RuntimeKernel) -> None:
    assert kernel.metadata.freeze.frozen is True


def assert_graph_mutable(kernel: RuntimeKernel) -> None:
    assert kernel.metadata.freeze.frozen is False
