from __future__ import annotations

from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.kernel.context import (
    ApplicationContext,
)
from template_app.bootstrap.lifecycle.manager import (
    LifecycleManager,
)
from template_app.bootstrap.lifecycle.registry import (
    LifecycleRegistry,
)
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.infrastructure.providers.registry import (
    InfrastructureRegistry,
)



def test_application_context_initial_state() -> None:
    runtime = RuntimeState(
        container=Container(),
        lifecycle_registry=LifecycleRegistry(),
        lifecycle_manager=LifecycleManager(
            registry=LifecycleRegistry(),
        ),
        infrastructure_registry=InfrastructureRegistry(),
    )

    context = ApplicationContext(runtime=runtime)

    assert context.app is None
    assert context.runtime is runtime
