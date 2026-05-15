from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    await connect_db()
    await connect_redis()

    yield

    await disconnect_redis()
    await disconnect_db()
