"""Transport runtime domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.transports.manager import TransportManager


@dataclass(slots=True)
class TransportRuntime:
    """
    Transport runtime domain.

    Responsibilities:
        - transport ownership
        - transport orchestration
    """

    manager: TransportManager
