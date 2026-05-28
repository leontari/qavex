from __future__ import annotations

import pytest

from template_app.runtime.container.container import Container

from template_app.runtime.infrastructure.infra import (
    CacheProvider,
    DatabaseProvider,
    QueueProvider,
)

from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)

from template_app.runtime.infrastructure.runtime import (
    InfrastructureRuntime,
)

from template_app.runtime.lifecycle.manager import (
    LifecycleManager,
)

from template_app.runtime.lifecycle.readiness import (
    ReadinessGate,
)

from template_app.runtime.lifecycle.registry import (
    LifecycleRegistry,
)

from template_app.runtime.lifecycle.runtime import (
    LifecycleRuntime,
)

from template_app.runtime.messaging.buses import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeQueryBus,
)

from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)

from template_app.runtime.messaging.runtime import (
    MessagingRuntime,
)

from template_app.runtime.modules.registry import (
    ModuleRegistry,
)

from template_app.runtime.modules.runtime import (
    ModuleRuntime,
)

from template_app.runtime.transports.manager import (
    TransportManager,
)

from template_app.runtime.transports.runtime import (
    TransportRuntime,
)

from template_app.runtime.kernel.runtime.state import (
    RuntimeState,
)


@pytest.fixture
def container() -> Container:
    return Container()


@pytest.fixture
def lifecycle_registry() -> LifecycleRegistry:
    return LifecycleRegistry()


@pytest.fixture
def readiness_gate() -> ReadinessGate:
    return ReadinessGate()


@pytest.fixture
def lifecycle_manager(
    lifecycle_registry: LifecycleRegistry,
) -> LifecycleManager:
    return LifecycleManager(
        _registry=lifecycle_registry,
    )


@pytest.fixture
def lifecycle_runtime(
    lifecycle_registry: LifecycleRegistry,
    lifecycle_manager: LifecycleManager,
    readiness_gate: ReadinessGate,
) -> LifecycleRuntime:
    return LifecycleRuntime(
        registry=lifecycle_registry,
        manager=lifecycle_manager,
        readiness=readiness_gate,
    )


@pytest.fixture
def infrastructure_registry() -> InfrastructureRegistry:
    return InfrastructureRegistry(
        cache=CacheProvider(
            "redis://localhost:6379",
        ),
        database=DatabaseProvider(
            "postgresql://localhost/test",
        ),
        queue=QueueProvider(
            ["localhost:9092"],
        ),
    )


@pytest.fixture
def infrastructure_runtime(
    infrastructure_registry: InfrastructureRegistry,
) -> InfrastructureRuntime:
    return InfrastructureRuntime(
        registry=infrastructure_registry,
    )


@pytest.fixture
def messaging_registry() -> RuntimeHandlerRegistry:
    return RuntimeHandlerRegistry()


@pytest.fixture
def event_bus(
    messaging_registry: RuntimeHandlerRegistry,
) -> RuntimeEventBus:
    return RuntimeEventBus(
        registry=messaging_registry,
    )


@pytest.fixture
def command_bus(
    messaging_registry: RuntimeHandlerRegistry,
) -> RuntimeCommandBus:
    return RuntimeCommandBus(
        registry=messaging_registry,
    )


@pytest.fixture
def query_bus(
    messaging_registry: RuntimeHandlerRegistry,
) -> RuntimeQueryBus:
    return RuntimeQueryBus(
        registry=messaging_registry,
    )


@pytest.fixture
def messaging_runtime(
    messaging_registry: RuntimeHandlerRegistry,
    event_bus: RuntimeEventBus,
    command_bus: RuntimeCommandBus,
    query_bus: RuntimeQueryBus,
) -> MessagingRuntime:
    return MessagingRuntime(
        registry=messaging_registry,
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )


@pytest.fixture
def transport_runtime() -> TransportRuntime:
    return TransportRuntime(
        manager=TransportManager(),
    )


@pytest.fixture
def module_runtime() -> ModuleRuntime:
    return ModuleRuntime(
        registry=ModuleRegistry(),
    )


@pytest.fixture
def runtime_state(
    container: Container,
    lifecycle_runtime: LifecycleRuntime,
    infrastructure_runtime: InfrastructureRuntime,
    messaging_runtime: MessagingRuntime,
    transport_runtime: TransportRuntime,
    module_runtime: ModuleRuntime,
) -> RuntimeState:
    return RuntimeState(
        container=container,
        lifecycle=lifecycle_runtime,
        infrastructure=infrastructure_runtime,
        messaging=messaging_runtime,
        transports=transport_runtime,
        modules=module_runtime,
    )
