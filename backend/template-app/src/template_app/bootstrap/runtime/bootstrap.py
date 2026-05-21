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
from template_app.bootstrap.messaging.runtime import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeHandlerRegistry,
    RuntimeQueryBus,
)
from template_app.bootstrap.modules import (
    # TODO: recheck this as now it's done via  MODULE_REGISTRY
    ModuleSetupContext,
    discover_modules,
    load_modules,
)
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.bootstrap.modules_definitions import MODULE_REGISTRY
from template_app.bootstrap.runtime.lifespan import create_lifespan
from template_app.bootstrap.runtime.state import RuntimeState


def bootstrap_application() -> RuntimeKernel:
    """
    Bootstrap runtime kernel.

    Responsibilities:
    - initialize runtime state
    - initialize infrastructure
    - initialize messaging
    - initialize FastAPi transport
    - initialize module system
    - register lifecycle hooks

    Returns:
        RuntimeKernel: fully initialized the application's kernel

    """
    ###############
    # DI container
    ###############
    container = Container()

    ############
    # lifecycle
    ############
    lifecycle_registry = LifecycleRegistry()

    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    #################
    # infrastructure
    #################

    infrastructure_registry = bootstrap_infrastructure()

    ############
    # messaging
    ############

    messaging_registry = RuntimeHandlerRegistry()

    event_bus = RuntimeEventBus(registry=messaging_registry)
    command_bus = RuntimeCommandBus(registry=messaging_registry)
    query_bus = RuntimeQueryBus(registry=messaging_registry)

    ###########################
    # the state of the runtime
    ###########################

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

    #################################
    # the context of the application
    #################################

    # TODO: rename to KernelContext? Frozen?
    context = ApplicationContext(runtime=runtime)

    kernel = RuntimeKernel(context=context)

    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(),
    )

    context.app = app

    # injection of lifespan AFTER the kernel's creation
    # app.router.lifespan_context = create_lifespan(kernel)

    ######################
    # APIs of the modules
    ######################

    runtime_api = ModuleRuntimeAPI(
        app=app,
        container=container,
        lifecycle_registry=lifecycle_registry,
    )

    infra_api = ModuleInfraAPI(
        registry=infrastructure_registry,
    )

    messaging_api = ModuleMessagingAPI(
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )

    ###################
    # modules' loading
    ###################

    manifests = discover_modules(
        MODULE_REGISTRY,
    )  # TODO: autodiscover modules

    for manifest in manifests:
        module_context = ModuleSetupContext(
            runtime=runtime_api,
            infra=infra_api,
            messaging=messaging_api,
            capabilities=manifest.capabilities,
        )

        load_modules(
            manifest=manifest,
            context=module_context,
        )

    #############################
    # infrastructure's lifecycle
    #############################

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
