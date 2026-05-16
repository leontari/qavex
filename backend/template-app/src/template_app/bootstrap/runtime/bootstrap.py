from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.modules import MODULES
from template_app.bootstrap.runtime.kernel import RuntimeKernel
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> RuntimeKernel:
    """Bootstrap application runtime kernel."""

    lifecycle_registry: LifecycleRegistry = LifecycleRegistry()

    container: Container = Container()

    lifecycle_manager: LifecycleManager = LifecycleManager(
        registry=lifecycle_registry,
    )

    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
    )

    temporary_app: FastAPI = FastAPI()

    context: ApplicationContext = ApplicationContext(
        app=temporary_app,
        runtime=runtime,
    )

    # TODO: check and maybe set default values to be able inject latter
    kernel: RuntimeKernel = RuntimeKernel(context=context)

    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(kernel),
    )

    context.app = app

    for module in MODULES:
        module.setup(context)

    return kernel
