"""ASGI application entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

if TYPE_CHECKING:
    from fastapi import FastAPI

context = bootstrap_application()

app: FastAPI = context.app
