"""Runtime metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.runtime.capabilities.models import (
        RuntimeCapabilities,
    )
    from template_app.runtime.kernel.runtime.descriptors.models import (
        RuntimeDescriptor,
    )
    from template_app.runtime.kernel.runtime.graph.freeze import (
        RuntimeGraphFreeze,
    )


@dataclass(slots=True, frozen=True)
class RuntimeMetadata:
    """
    Runtime metadata.

    Responsibilities:
        - runtime descriptor ownership
        - runtime capability ownership
        - freeze ownership

    Notes:
        Metadata is not part of RuntimeState.

        Metadata belongs to RuntimeKernel.

    """

    descriptor: RuntimeDescriptor

    capabilities: RuntimeCapabilities

    freeze: RuntimeGraphFreeze
