from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.capabilities.runtime import (
    build_runtime_capabilities,
)


def test_runtime_capabilities_created(kernel: RuntimeKernel) -> None:
    capabilities = build_runtime_capabilities(kernel.runtime)

    assert capabilities.lifecycle is True
