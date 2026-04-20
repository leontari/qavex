"""WebSocket endpoint."""

from fastapi import APIRouter, WebSocket
from market_data.modules.ticks.service import TickService


router = APIRouter()
service = TickService()

@router.websocket("/ws/ticks")
async def ticks_ws(ws: WebSocket):
    await ws.accept()

    async for tick in service.stream_ticks():
        await ws.send_json(tick)
