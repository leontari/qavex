from template_app.runtime.runtime.capabilities.runtime import (
    build_runtime_capabilities,
)
from tests.factories.runtime import build_runtime_state


def test_runtime_capabilities_created() -> None:
    runtime = build_runtime_state()

    capabilities = build_runtime_capabilities(runtime)

    assert capabilities.lifecycle is True
