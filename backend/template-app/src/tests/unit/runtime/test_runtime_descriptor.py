from template_app.runtime.runtime.descriptors.runtime import (
    build_runtime_descriptor,
)
from tests.factories.runtime import build_runtime_state


def test_runtime_descriptor_created() -> None:
    runtime = build_runtime_state()

    descriptor = build_runtime_descriptor(runtime)

    assert descriptor.modules >= 0
