from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.bootstrap.events.bus import EventBus
from template_app.bootstrap.events.dispatcher import EventDispatcher
from template_app.bootstrap.events.registry import EventRegistry
from template_app.bootstrap.infrastructure import bootstrap_infrastructure
from template_app.bootstrap.kernel import (
    ApplicationContext,
    Container,
    RuntimeKernel,
)
from template_app.bootstrap.lifecycle import (
    LifecycleHook,
    LifecycleManager,
    LifecycleRegistry,
)
from template_app.bootstrap.modules import (
    ModuleRegistry,  # TODO: recheck this as now it's done via  MODULE_REGISTRY
    ModuleSetupContext,
    discover_modules,
    load_modules,
)
from template_app.bootstrap.modules_definitions import MODULE_REGISTRY
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> RuntimeKernel:
    """Bootstrap runtime kernel."""

    lifecycle_registry = LifecycleRegistry()
    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    infrastructure_registry = bootstrap_infrastructure()

    container = Container()

    # assemble event_bus instance
    event_registry = EventRegistry()
    event_dispatcher = EventDispatcher(registry=event_registry)
    event_bus = EventBus(registry=event_registry, dispatcher=event_dispatcher)

    # create RuntimeState instance and inject its dependencies
    runtime = RuntimeState(
        container=container,
        event_bus=event_bus,
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

    # register modules
    module_context = ModuleSetupContext(_kernel=kernel)
    manifests = discover_modules(MODULE_REGISTRY)
    load_modules(manifests=manifests, context=module_context)

    # register infrastructure providers
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
