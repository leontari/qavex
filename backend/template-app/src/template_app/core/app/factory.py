import logging
from fastapi import FastAPI


def create_app() -> FastAPI:

    logger = logging.getLogger(__name__)

    app = FastAPI()
    logger.info(f"Application starting...")

    return app
