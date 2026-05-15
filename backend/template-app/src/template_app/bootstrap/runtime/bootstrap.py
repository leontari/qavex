from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.modules import MODULES
from template_app.bootstrap.runtime.lifespan import lifespan
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry


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

    # TODO: recheck this
    app.state.container = container
    app.state.lifecycle_registry = lifecycle_registry
    app.state.lifecycle_manager = lifecycle_manager

    for module in MODULES:
        module.setup(app, container)

    return ApplicationContext(
        app=app,
        container=container,
    )
