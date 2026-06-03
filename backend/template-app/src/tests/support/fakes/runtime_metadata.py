from __future__ import annotations

from template_app.runtime.kernel.runtime.capabilities.runtime import (
    build_runtime_capabilities,
)
from template_app.runtime.kernel.runtime.descriptors.runtime import (
   build_runtime_descriptor,
)
from template_app.runtime.kernel.runtime.graph.freeze import (
    RuntimeGraphFreeze,
)
from template_app.runtime.kernel.runtime.metadata import (
    RuntimeMetadata,
)
from template_app.runtime.kernel.runtime.state import RuntimeState


def build_fake_metadata(runtime: RuntimeState) -> RuntimeMetadata:
    return RuntimeMetadata(
        descriptor=build_runtime_descriptor(runtime),
        capabilities=build_runtime_capabilities(runtime),
        freeze=RuntimeGraphFreeze(),
    )
