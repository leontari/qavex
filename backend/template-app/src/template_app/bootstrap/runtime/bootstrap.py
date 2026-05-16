from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.modules import MODULES
from template_app.bootstrap.runtime.lifespan import lifespan
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> ApplicationContext:
    """
    Create fully configured application runtime.

    Returns:
        ApplicationContext: the fully configured application instance

    """
    lifecycle_registry: LifecycleRegistry = LifecycleRegistry()

    app: FastAPI = FastAPI(
        title="template-app",
        lifespan=lifespan,
    )

    container: Container = Container()

    lifecycle_manager: LifecycleManager = LifecycleManager(
        registry=lifecycle_registry,
    )

    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
    )

    context: ApplicationContext = ApplicationContext(
        app=app,
        runtime=runtime,
    )

    app.state.context = context

    for module in MODULES:
        module.setup(context)

    return context
