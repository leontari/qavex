from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.kernel import (
    KernelContext,
)
from tests.factories.runtime import (
    build_runtime_state,
)


def build_kernel_context() -> KernelContext:

    return KernelContext(
        runtime=build_runtime_state(),
        app=FastAPI(title="template-app"),
    )
