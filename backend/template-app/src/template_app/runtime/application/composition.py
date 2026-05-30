"""
Application composition contracts.

Responsibilities:
    - application composition state
    - transport installation ownership
    - freeze orchestration ownership
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel
    from template_app.runtime.transports.contracts import Transport


@dataclass(slots=True)
class ApplicationComposition:
    """
    Mutable application composition.

    Responsibilities:
        - kernel ownership
        - transport collection
        - pre-freeze composition

    Notes:
        This object exists only during
        application assembly phase.

    """

    kernel: RuntimeKernel

    transports: list[Transport] = field(default_factory=list)
