"""startup/shutdown."""
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    # startup
    print("Starting market-data service")
    yield
    # shutdown
    print("Stopping market-data service")
