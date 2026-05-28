"""Application runtime composition graph."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.kernel.runtime.capabilities.models import (
    RuntimeCapabilities,
)
from template_app.runtime.kernel.runtime.descriptors.runtime import (
    RuntimeDescriptor,
)
from template_app.runtime.kernel.runtime.graph.freeze import RuntimeGraphFreeze

if TYPE_CHECKING:
    from template_app.runtime.container.container import Container
    from template_app.runtime.infrastructure.runtime import (
        InfrastructureRuntime,
    )
    from template_app.runtime.lifecycle.runtime import LifecycleRuntime
    from template_app.runtime.messaging.runtime import MessagingRuntime
    from template_app.runtime.modules.runtime import ModuleRuntime
    from template_app.runtime.transports.runtime import TransportRuntime


@dataclass(slots=True)
class RuntimeState:
    """
    Application runtime state.

    Responsibilities:
        - runtime ownership
        - composition graph ownership
        - runtime domains ownership

    """

    # freeze: RuntimeGraphFreeze
    #
    # capabilities: RuntimeCapabilities
    #
    # descriptor: RuntimeDescriptor

    container: Container

    lifecycle: LifecycleRuntime

    infrastructure: InfrastructureRuntime

    messaging: MessagingRuntime

    transports: TransportRuntime

    modules: ModuleRuntime
