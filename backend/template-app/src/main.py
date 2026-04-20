import logging

from fastapi import FastAPI

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
