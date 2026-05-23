from __future__ import annotations

from typing import TYPE_CHECKING, cast

from fastapi import FastAPI
from starlette.routing import Router

from template_app.runtime.transports.http.lifespan import create_lifespan

if TYPE_CHECKING:
    from template_app.runtime.kernel import RuntimeKernel


def create_transport() -> FastAPI:
    return FastAPI(title="template-app")


def configure_transport(app: FastAPI, kernel: RuntimeKernel) -> None:
    """Configure transport runtime integrations."""

    cast(
        Router,
        app.router,
    ).lifespan_context = create_lifespan(kernel)
