from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.infrastructure import bootstrap_infrastructure
from template_app.bootstrap.modules import MODULES
from template_app.bootstrap.runtime.hooks import LifecycleHook
from template_app.bootstrap.runtime.kernel import RuntimeKernel
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState

if TYPE_CHECKING:
    from template_app.infrastructure.providers.registry import (
        InfrastructureRegistry,
    )


def bootstrap_application() -> RuntimeKernel:
    """Bootstrap application runtime kernel."""

    lifecycle_registry: LifecycleRegistry = LifecycleRegistry()
    infrastructure_registry: InfrastructureRegistry = (
        bootstrap_infrastructure()
    )

    container: Container = Container()

    lifecycle_manager: LifecycleManager = LifecycleManager(
        registry=lifecycle_registry,
    )

    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
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

    # register modules
    for module in MODULES:
        module.setup(context)

    # TODO: check shutdown hook and a better way
    # integrate infrastructure providers
    for provider in infrastructure_registry.providers:
        lifecycle_registry.register_startup(
            LifecycleHook(
                name=f"{provider.name}.startup",
                handler=provider.startup,
            )
        )

        lifecycle_registry.register_shutdown(
            LifecycleHook(
                name=f"{provider.name}.shutdown",
                handler=provider.shutdown,
            )
        )

    return kernel
