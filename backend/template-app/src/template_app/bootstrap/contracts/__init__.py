"""Protocols/contracts."""

from __future__ import annotations

from template_app.bootstrap.contracts.dependencies import (
    DependencyProvider,
)
from template_app.bootstrap.contracts.infrastructure import (
    InfrastructureProvider,
)
from template_app.bootstrap.contracts.modules import ModuleProtocol
from template_app.bootstrap.contracts.types import DependencyScope

__all__ = [
    "DependencyProvider",
    "DependencyScope",
    "InfrastructureProvider",
    "ModuleProtocol",
]
