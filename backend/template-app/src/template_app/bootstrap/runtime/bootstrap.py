"""Composition root."""

from __future__ import annotations

from fastapi import FastAPI

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
from template_app.bootstrap.messaging.runtime.command_bus import (
    RuntimeCommandBus,
)
from template_app.bootstrap.messaging.runtime.event_bus import (
    RuntimeEventBus,
)
from template_app.bootstrap.messaging.runtime.query_bus import (
    RuntimeQueryBus,
)
from template_app.bootstrap.messaging.runtime.registry import (
    RuntimeHandlerRegistry,
)
from template_app.bootstrap.modules import (
    # TODO: recheck this as now it's done via  MODULE_REGISTRY
    ModuleSetupContext,
    discover_modules,
    load_modules,
)
from template_app.bootstrap.modules_definitions import MODULE_REGISTRY
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> RuntimeKernel:
    """Bootstrap runtime kernel."""

    # DI
    container = Container()

    # lifecycle
    lifecycle_registry = LifecycleRegistry()
    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    # infrastructure
    infrastructure_registry = bootstrap_infrastructure()

    # messaging
    messaging_registry = RuntimeHandlerRegistry()
    event_bus = RuntimeEventBus(registry=messaging_registry)
    command_bus = RuntimeCommandBus(registry=messaging_registry)
    query_bus = RuntimeQueryBus(registry=messaging_registry)

    # runtime state
    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
        messaging_registry=messaging_registry,
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )

    # transport
    app = FastAPI(title="template-app")

    # immutable application context
    context = ApplicationContext(runtime=runtime, app=app)

    # kernel
    kernel = RuntimeKernel(context=context)

    # inject lifespan AFTER kernel creation
    app.router.lifespan_context = create_lifespan(kernel)

    # module system
    module_context = ModuleSetupContext(_kernel=kernel)
    manifests = discover_modules(MODULE_REGISTRY)
    load_modules(manifests=manifests, context=module_context)

    # infrastructure Lifecycle integration
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
