from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.bootstrap.infrastructure import bootstrap_infrastructure
from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.kernel.context import ApplicationContext
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from template_app.bootstrap.lifecycle.hooks import LifecycleHook
from template_app.bootstrap.lifecycle.manager import LifecycleManager
from template_app.bootstrap.lifecycle.registry import LifecycleRegistry
from template_app.bootstrap.modules.loader import load_modules
from template_app.bootstrap.modules.registry import module_registry
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> RuntimeKernel:
    """Bootstrap runtime kernel."""

    lifecycle_registry = LifecycleRegistry()

    infrastructure_registry = bootstrap_infrastructure()

    container = Container()

    lifecycle_manager = LifecycleManager(
        registry=lifecycle_registry,
    )

    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
    )

    context = ApplicationContext(runtime=runtime)

    kernel = RuntimeKernel(context=context)

    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(kernel),
    )

    context.app = app

    load_modules(
        kernel=kernel,
        registry=module_registry,
    )

    for provider in infrastructure_registry.providers:
        lifecycle_registry.register_startup(
            LifecycleHook(
                name=f"{provider.name}.startup",
                handler=provider.startup,
            ),
        )

        lifecycle_registry.register_shutdown(
            LifecycleHook(
                name=f"{provider.name}.shutdown",
                handler=provider.shutdown,
            ),
        )

    return kernel
