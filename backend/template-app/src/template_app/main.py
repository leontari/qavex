"""
Development entry point.

This file is used ONLY when running the app locally.
Command to start the app form the project root folder:
    python backend/template-app/src/template_app/main.py

Production must use:
    uvicorn ingestor:app --host 0.0.0.0 --port 8000 --log-config path/to/logging.json

"""

from fastapi import FastAPI
from core.config import settings
from core.logging import setup_logging
# from api.router import api_router
# from observability.router import observability_router


def create_app() -> FastAPI:
    app: FastAPI = FastAPI()

    #app.include_router(api_router)
    #app.include_router(observability_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    import logging

    setup_logging(settings.log_level)
    logging.info("Starting application")

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
    )
