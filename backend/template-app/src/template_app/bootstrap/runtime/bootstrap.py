"""Composition root."""

from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.dispatching.commands.dispatcher import (
    CommandDispatcher,
)
from template_app.bootstrap.dispatching.queries.dispatcher import (
    QueryDispatcher,
)
from template_app.bootstrap.dispatching.registry import (
    MessageHandlerRegistry,
)
from template_app.bootstrap.infrastructure import bootstrap_infrastructure
from template_app.bootstrap.integration.bus import (
    RuntimeIntegrationBus,
)
from template_app.bootstrap.integration.registry import (
    IntegrationHandlerRegistry,
)
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

    lifecycle_registry = LifecycleRegistry()
    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    infrastructure_registry = bootstrap_infrastructure()

    # in-memory runtime inter-module data communication bus
    integration_registry = IntegrationHandlerRegistry()
    integration_bus = RuntimeIntegrationBus(registry=integration_registry)

    # in-memory runtime inter-module commands/queries bus
    message_registry = MessageHandlerRegistry()
    command_dispatcher = CommandDispatcher(registry=message_registry)
    query_dispatcher = QueryDispatcher(registry=message_registry)

    # DI container
    container = Container()

    # create RuntimeState instance and inject its dependencies
    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
        integration_registry=integration_registry,
        integration_bus=integration_bus,
        message_registry=message_registry,
        command_dispatcher=command_dispatcher,
        query_dispatcher=query_dispatcher,
    )

    # build kernel
    context = ApplicationContext(runtime=runtime)
    kernel = RuntimeKernel(context=context)
    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(kernel),
    )
    context.app = app

    # register modules in kernel
    module_context = ModuleSetupContext(_kernel=kernel)
    manifests = discover_modules(MODULE_REGISTRY)
    load_modules(manifests=manifests, context=module_context)

    # register infrastructure providers in kernel
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
