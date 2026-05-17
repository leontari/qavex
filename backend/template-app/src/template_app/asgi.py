"""ASGI application entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.runtime.kernel import RuntimeKernel

kernel: RuntimeKernel = bootstrap_application()

app: FastAPI = kernel.context.app
