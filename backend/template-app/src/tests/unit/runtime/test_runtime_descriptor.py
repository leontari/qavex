from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.descriptors.runtime import (
    build_runtime_descriptor,
)


def test_runtime_descriptor_created(kernel: RuntimeKernel) -> None:
    descriptor = build_runtime_descriptor(kernel.runtime)

    assert descriptor.modules >= 0
