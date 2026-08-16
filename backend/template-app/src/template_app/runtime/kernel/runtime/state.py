"""Application runtime composition graph."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container import Container
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
    Application runtime composition graph.

    Responsibilities:
        - runtime ownership
        - dependency ownership
        - runtime domains ownership
        - runtime topology

    Notes:
        RuntimeState contains only live runtime domains.

        No metadata is stored here.

    """

    container: Container

    lifecycle: LifecycleRuntime

    infrastructure: InfrastructureRuntime

    messaging: MessagingRuntime

    transports: TransportRuntime

    modules: ModuleRuntime
