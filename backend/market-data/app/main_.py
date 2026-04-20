"""Entrypoint."""

from fastapi import FastAPI
from market_data.modules.ticks.ws import router as ws_router
from market_data.core.lifecycle import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(ws_router)
