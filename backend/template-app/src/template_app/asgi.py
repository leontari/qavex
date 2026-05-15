"""ASGI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

context = bootstrap_application()

app: FastAPI = context.app
