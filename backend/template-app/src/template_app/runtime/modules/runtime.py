"""Module runtime domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.modules.registry import ModuleRegistry


@dataclass(slots=True)
class ModuleRuntime:
    """
    Module runtime domain.

    Responsibilities:
        - module registry ownership
        - plugin ownership
    """

    registry: ModuleRegistry
