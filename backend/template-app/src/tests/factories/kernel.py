from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel.context import ApplicationContext
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from template_app.bootstrap.runtime.lifespan import create_lifespan
from tests.factories.runtime import build_runtime_state


def build_kernel() -> RuntimeKernel:
    """Build runtime kernel."""

    runtime = build_runtime_state()
    context = ApplicationContext(runtime=runtime)
    kernel = RuntimeKernel(context=context)
    app = FastAPI(lifespan=create_lifespan(kernel))

    context.app = app

    return kernel
