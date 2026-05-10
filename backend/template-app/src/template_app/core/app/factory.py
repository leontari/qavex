from __future__ import annotations

import logging

from fastapi import FastAPI


def create_app() -> FastAPI:

    logger = logging.getLogger(__name__)

    app = FastAPI()
    logger.info("Application starting...")

    return app
