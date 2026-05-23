"""
ASGI application entry point.

This module initializes logging and constructs the FastAPI application
instance used by external ASGI servers such as Uvicorn or Gunicorn.

It is intentionally minimal and contains no development-only logic.
Production runners should import the `app` object from this module, e.g.:

    uvicorn template_app.asgi:app

or import from package. The `app` will be reexported from this module:

    uvicorn template_app:app

The application factory and logging setup are delegated to the core
infrastructure modules to keep the ASGI entry point lightweight and
side effect free.

asgi.py
  ↓
create_app()
  ↓
FastAPI(lifespan)
  ↓
LifecycleManager
  ↓
┌──────────────────────┐
│ startup              │
│  ├── db              │
│  ├── cache           │
│  ├── health system   │
│  ├── bg tasks        │
│  └── ready state     │
└──────────────────────┘

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.runtime import bootstrap_application
from template_app.core_.app_.factory import create_app
from template_app.core_.app_.logger import setup_logging

if TYPE_CHECKING:
    from fastapi import FastAPI


# setup_logging()

context = bootstrap_application()

app: FastAPI = context.app


# """
# Production ASGI application entry point.
#
# This module is responsible for:
#
# - logging initialization
# - lifecycle manager initialization
# - FastAPI application creation
# - startup/shutdown orchestration wiring
#
# The module intentionally contains no development-only execution logic.
#
# Production servers should import the `app` object directly:
#
#     uvicorn template_app.asgi:app
#
# or:
#
#     uvicorn template_app:app
# """

# from __future__ import annotations
#
# from contextlib import asynccontextmanager
# from typing import AsyncIterator
#
# from fastapi import FastAPI
#
# from template_app.api.router import api_router
# from template_app.config.app import config
# from template_app.config.settings import settings
# from template_app.core.app.logger import (
#     setup_logging,
# )
# from template_app.core.lifecycle import (
#     LifecycleManager,
# )
#
# setup_logging()
#
# lifecycle_manager = LifecycleManager()
#
#
# @asynccontextmanager
# async def lifespan(
#     app: FastAPI,
# ) -> AsyncIterator[None]:
#     """
#     FastAPI application lifespan manager.
#
#     This lifecycle context coordinates:
#
#     - runtime startup orchestration
#     - scheduler initialization
#     - background task management
#     - graceful shutdown
#
#     Args:
#         app:
#             FastAPI application instance.
#     """
#     await lifecycle_manager.startup(app)
#
#     yield
#
#     await lifecycle_manager.shutdown(app)
#
#
# app = FastAPI(
#     title=config.APP_TITLE,
#     description=config.APP_DESCRIPTION,
#     version=config.APP_VERSION,
#     docs_url=config.DOCS_URL,
#     redoc_url=config.REDOC_URL,
#     openapi_url=config.OPENAPI_URL,
#     debug=settings.DEBUG,
#     lifespan=lifespan,
# )
#
# app.include_router(api_router)
