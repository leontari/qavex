"""Module static metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.modules.capabilities import ModuleCapability
    from template_app.runtime.modules.contracts import ModuleProtocol


@dataclass(frozen=True, slots=True)
class ModuleManifest:
    """Static module metadata."""

    name: str
    module: ModuleProtocol
    capabilities: frozenset[ModuleCapability] = field(
        default_factory=frozenset
    )
    enabled: bool = True
