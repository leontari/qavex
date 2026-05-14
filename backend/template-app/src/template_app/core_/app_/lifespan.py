@asynccontextmanager
async def lifespan(app):
    await connect_database()
    yield
