"""Module static metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.contracts import ModuleProtocol
    from template_app.bootstrap.modules.capabilities import ModuleCapability


@dataclass(frozen=True, slots=True)
class ModuleManifest:
    """Static module metadata."""

    name: str
    module: ModuleProtocol
    capabilities: frozenset[ModuleCapability]
    enabled: bool = True
