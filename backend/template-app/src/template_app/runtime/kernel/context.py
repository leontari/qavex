"""Kernel context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from .state import RuntimeState


@dataclass(slots=True, frozen=True)
class KernelContext:
    """Immutable runtime composition graph."""

    runtime: RuntimeState
