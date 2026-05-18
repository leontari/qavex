from __future__ import annotations

import pytest
from fastapi import FastAPI

from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.kernel.context import (
    ApplicationContext,
)
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from template_app.bootstrap.lifecycle.manager import (
    LifecycleManager,
)
from template_app.bootstrap.lifecycle.registry import (
    LifecycleRegistry,
)
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)



def build_kernel() -> RuntimeKernel:
    registry = LifecycleRegistry()

    runtime = RuntimeState(
        container=Container(),
        lifecycle_registry=registry,
        lifecycle_manager=LifecycleManager(registry=registry),
        infrastructure_registry=InfrastructureRegistry(),
    )

    context = ApplicationContext(runtime=runtime)

    return RuntimeKernel(context=context)



def test_kernel_requires_initialized_app() -> None:
    kernel = build_kernel()

    with pytest.raises(RuntimeError):
        _ = kernel.app



def test_kernel_returns_app() -> None:
    kernel = build_kernel()

    app = FastAPI()

    kernel.context.app = app

    assert kernel.app is app
