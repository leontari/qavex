"""
External adapters.

Responsible for:
    external systems
"""

from __future__ import annotations

from template_app.bootstrap.infrastructure.bootstrap import (
    bootstrap_infrastructure,
)
from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)

__all__ = [
    "InfrastructureRegistry",
    "bootstrap_infrastructure",
]
