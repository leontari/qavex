"""
Composition root.

Responsibilities:
    - build runtime graph
    - wire dependencies
    - construct kernel
"""

from __future__ import annotations

from template_app.runtime.container.container import Container
from template_app.runtime.infrastructure.infra import (
    CacheProvider,
    DatabaseProvider,
    QueueProvider,
)
from template_app.runtime.infrastructure.registry import InfrastructureRegistry
from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.state import RuntimeState
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
from template_app.runtime.runtime.capabilities.runtime import (
    build_runtime_capabilities,
)
from template_app.runtime.runtime.descriptors.runtime import (
    build_runtime_descriptor,
)
from template_app.runtime.runtime.graph.freeze import RuntimeGraphFreeze
from template_app.runtime.runtime.graph.validator import RuntimeGraphValidator
from template_app.runtime.transports.manager import TransportManager
from template_app.runtime.transports.runtime import TransportRuntime


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

    infra_registry = InfrastructureRegistry(
        cache=CacheProvider(),
        database=DatabaseProvider(),
        queue=QueueProvider(),
    )

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

    ###############
    # create kernel
    ###############

    runtime.freeze = RuntimeGraphFreeze()
    runtime.capabilities = build_runtime_capabilities(runtime)
    runtime.descriptor = build_runtime_descriptor(runtime)
    RuntimeGraphValidator.validate(runtime)
    runtime.freeze.freeze()

    return RuntimeKernel.create(runtime=runtime)
