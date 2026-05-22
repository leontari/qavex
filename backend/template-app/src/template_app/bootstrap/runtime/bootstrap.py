"""Composition root."""

from __future__ import annotations

from template_app.bootstrap.infrastructure import bootstrap_infrastructure
from template_app.bootstrap.kernel import (
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
from template_app.bootstrap.modules.setup import setup_modules
from template_app.bootstrap.modules_definitions import MODULE_REGISTRY
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.bootstrap.runtime.transport import (
    configure_transport,
    create_transport,
)


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

    ##############
    # data busses
    ##############

    messaging_registry = RuntimeHandlerRegistry()

    event_bus = RuntimeEventBus(registry=messaging_registry)
    command_bus = RuntimeCommandBus(registry=messaging_registry)
    query_bus = RuntimeQueryBus(registry=messaging_registry)

    #######################
    # Kernel runtime state
    #######################

    runtime_state = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
        messaging_registry=messaging_registry,
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )

    #########
    # Kernel
    #########

    # HTTP transport
    app = create_transport()

    # create kernel runtime
    kernel = RuntimeKernel.create(
        runtime=runtime_state,
        app=app,
    )

    # bind transport runtime integrations
    configure_transport(
        app=kernel.app,
        kernel=kernel,
    )

    ##################
    # Install modules
    ##################

    setup_modules(
        kernel=kernel,
        registry=MODULE_REGISTRY,
    )

    ##########################################
    # Register the infrastructure's lifecycle
    ##########################################

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
