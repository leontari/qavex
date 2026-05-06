from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.observability.router import observability_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router)
    app.include_router(observability_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    import logging

    setup_logging(settings.log_level)
    logging.info("Starting application")

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
    )
