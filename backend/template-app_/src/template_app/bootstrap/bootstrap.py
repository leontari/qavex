"""Main bootstrap module."""

from __future__ import annotations

from fastapi import FastAPI

from template_app.api.router import register_routes
from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.core_.app_.exception_handlers import (
    register_exception_handlers,
)
from template_app.core_.app_.middleware import register_middleware


def bootstrap_application() -> ApplicationContext:
    app = FastAPI()

    container = Container()

    register_middleware(app)
    register_exception_handlers(app)
    register_routes(app)

    app.state.container = container

    return ApplicationContext(
        app=app,
        container=container,
    )


# def bootstrap_application() -> ApplicationContext:
#     settings = bootstrap_settings()
#
#     configure_logging(settings)
#
#     container = bootstrap_container(settings)
#
#     app = bootstrap_fastapi(settings)
#
#     bootstrap_middlewares(app)
#
#     bootstrap_routes(app)
#
#     bootstrap_exception_handlers(app)
#
#     bootstrap_lifecycle(app, container)
#
#     return ApplicationContext(
#         app=app,
#         container=container,
#     )
