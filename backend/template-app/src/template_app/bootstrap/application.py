from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.runtime.state import RuntimeState


@dataclass(slots=True)
class ApplicationContext:
    """Runtime application context."""

    app: FastAPI
    runtime: RuntimeState
