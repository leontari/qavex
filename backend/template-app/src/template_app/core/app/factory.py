"""
Application factory.

This module defines the create_app() function, which constructs and
configures the FastAPI application instance. The factory pattern ensures
that the application can be created consistently across environments:
local development, Docker, and wheel-based installations.
"""

from __future__ import annotations

import logging
# from contextlib import asynccontextmanager

from fastapi import FastAPI

# from template_app.api.router import api_router
# from template_app.observability.router import observability_router
# from template_app.api.health import (
#     health_router,
#     live_router,
#     metrics_router,
#     ready_router,
# )
from template_app.config.app import config
from template_app.config.settings import settings
# from template_app.core.lifecycle.manager import LifecycleManager

# lifecycle = LifecycleManager()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await lifecycle.startup(app)
#     yield
#     await lifecycle.shutdown(app)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Returns:
        FastAPI: Fully initialized FastAPI application.

    """
    logger = logging.getLogger(__name__)

    logger.info("Creating the application...")

    app = FastAPI(
        # static application settings
        # title=config.APP_TITLE,
        # description=config.APP_DESCRIPTION,
        # version=config.APP_VERSION,
        # docs_url=config.DOCS_URL,
        # redoc_url=config.REDOC_URL,
        # openapi_url=config.OPENAPI_URL,
        # # environment-driven application settings
        # debug=settings.DEBUG,
        # # lifecycle engine injection
        # lifespan=lifespan,
    )

    logger.info("The application is created")

    # Register routers
    # app.include_router(api_router, prefix="/api")
    # app.include_router(observability_router, prefix="/observability")
    # app.include_router(live_router)
    # app.include_router(ready_router)
    # app.include_router(health_router)
    # app.include_router(metrics_router)

    return app
