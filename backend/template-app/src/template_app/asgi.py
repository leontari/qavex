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

from template_app.core.app.factory import create_app
from template_app.core.app.logger import setup_logging

if TYPE_CHECKING:
    from fastapi import FastAPI


def __get_app_instance() -> FastAPI:
    setup_logging()
    return create_app()


app: FastAPI = __get_app_instance()
