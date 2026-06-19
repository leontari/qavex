"""Scope subsystem."""

from __future__ import annotations

from .context import ScopeContext
from .handle import ScopeHandle
from .manager import ScopeManager
from .scope import ScopeID, ScopeSnapshot, ScopeState

__all__ = (
    "ScopeContext",
    "ScopeHandle",
    "ScopeID",
    "ScopeManager",
    "ScopeSnapshot",
    "ScopeState",
)
