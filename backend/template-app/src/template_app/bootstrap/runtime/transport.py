from __future__ import annotations

from typing import TYPE_CHECKING, cast

from starlette.routing import Router

from template_app.bootstrap.runtime.lifespan import create_lifespan

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.kernel import RuntimeKernel


def configure_transport(app: FastAPI, kernel: RuntimeKernel) -> None:
    """Configure transport runtime integrations."""

    cast(
        Router,
        app.router,
    ).lifespan_context = create_lifespan(kernel)
