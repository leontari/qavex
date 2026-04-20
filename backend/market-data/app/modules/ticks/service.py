"""Business-logic."""
from market_data.modules.ticks.stream import RedisTickStream


class TickService:
    def __init__(self):
        self.stream = RedisTickStream()

    async def stream_ticks(self):
        async for tick in self.stream.subscribe():
            yield tick
