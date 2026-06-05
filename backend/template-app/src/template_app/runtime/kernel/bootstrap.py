"""
Composition root.

Responsibilities:
    - build runtime graph
    - wire dependencies
    - construct kernel
"""

from __future__ import annotations

from template_app.launcher.exceptions import CompositionViolationError
from template_app.runtime.container import Container
from template_app.runtime.infrastructure.factories import (
    bootstrap_infrastructure,
)
from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.capabilities.runtime import (
    build_runtime_capabilities,
)
from template_app.runtime.kernel.runtime.descriptors.runtime import (
    build_runtime_descriptor,
)
from template_app.runtime.kernel.runtime.graph.freeze import (
    RuntimeGraphFreeze,
)
from template_app.runtime.kernel.runtime.metadata import RuntimeMetadata
from template_app.runtime.kernel.runtime.state import RuntimeState
from template_app.runtime.lifecycle.manager import LifecycleManager
from template_app.runtime.lifecycle.readiness import ReadinessGate
from template_app.runtime.lifecycle.registry import LifecycleRegistry
from template_app.runtime.lifecycle.runtime import LifecycleRuntime
from template_app.runtime.messaging.buses import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeQueryBus,
)
from template_app.runtime.messaging.registry import RuntimeHandlerRegistry
from template_app.runtime.messaging.runtime import MessagingRuntime
from template_app.runtime.modules.registry import ModuleRegistry
from template_app.runtime.modules.runtime import ModuleRuntime
from template_app.runtime.transports.manager import TransportManager
from template_app.runtime.transports.runtime import TransportRuntime

__ALLOW_BOOTSTRAP = False


def enable_builder_bootstrap() -> None:
    global __ALLOW_BOOTSTRAP
    __ALLOW_BOOTSTRAP = True


def disable_builder_bootstrap() -> None:
    global __ALLOW_BOOTSTRAP
    __ALLOW_BOOTSTRAP = False


def bootstrap_kernel() -> RuntimeKernel:
    """
    Build runtime kernel composition graph.

    Responsibilities:
        - runtime graph assembly
        - runtime domain wiring
        - dependency ownership composition

    Returns:
        RuntimeKernel:
            fully initialized runtime kernel

    """
    if not __ALLOW_BOOTSTRAP:
        msg = (
            "RuntimeKernel must be created only through "
            "ApplicationBuilder.create()"
        )
        raise CompositionViolationError(
            msg,
        )

    #################
    # shared runtimes
    #################
    container = Container()

    #################
    # Lifecycle graph
    #################
    lifecycle_registry = LifecycleRegistry()
    readiness_gate = ReadinessGate()

    lifecycle_manager = LifecycleManager(_registry=lifecycle_registry)

    lifecycle_runtime = LifecycleRuntime(
        registry=lifecycle_registry,
        manager=lifecycle_manager,
        readiness=readiness_gate,
    )

    ##################
    # data buses graph
    ##################

    handler_registry = RuntimeHandlerRegistry()

    event_bus = RuntimeEventBus(registry=handler_registry)
    command_bus = RuntimeCommandBus(registry=handler_registry)
    query_bus = RuntimeQueryBus(registry=handler_registry)

    messaging_runtime = MessagingRuntime(
        registry=handler_registry,
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )

    ######################
    # infrastructure graph
    ######################

    infra_registry = bootstrap_infrastructure()
    infrastructure_runtime = InfrastructureRuntime(
        registry=infra_registry,
    )

    #################
    # transport graph
    #################

    transport_runtime = TransportRuntime(
        manager=TransportManager(),
    )

    ##############
    # module graph
    ##############

    module_runtime = ModuleRuntime(
        registry=ModuleRegistry(),
    )

    #################
    # compose runtime
    #################

    runtime = RuntimeState(
        container=container,
        lifecycle=lifecycle_runtime,
        infrastructure=infrastructure_runtime,
        messaging=messaging_runtime,
        transports=transport_runtime,
        modules=module_runtime,
    )

    ##########
    # metadata
    ##########

    metadata = RuntimeMetadata(
        descriptor=build_runtime_descriptor(runtime),
        capabilities=build_runtime_capabilities(runtime),
        freeze=RuntimeGraphFreeze(),
    )

    return RuntimeKernel.create(
        runtime=runtime,
        metadata=metadata,
    )
