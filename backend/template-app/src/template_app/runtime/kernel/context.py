"""Kernel context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.runtime.state import RuntimeState


@dataclass(slots=True, frozen=True)
class KernelContext:
    """
    Immutable runtime composition graph.

    Responsibilities:
        - immutable runtime graph exposure
        - runtime ownership boundary
        - dependency boundary

    Notes:
        Context intentionally contains only RuntimeState.

        Runtime metadata belongs to RuntimeKernel and is not
        considered part of the runtime graph.

    """

    runtime: RuntimeState
