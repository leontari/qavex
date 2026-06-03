"""Infrastructure runtime domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.infrastructure.registry import (
        InfrastructureRegistry,
    )


@dataclass(slots=True)
class InfrastructureRuntime:
    """
    Infrastructure runtime domain.

    Responsibilities:
        - infrastructure registry ownership

    """

    registry: InfrastructureRegistry
