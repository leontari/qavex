"""Redis pub/sub logic, the stream's core."""
import json
from market_data.infrastructure.redis.pubsub import get_pubsub


class RedisTickStream:
    CHANNEL = "ticks"

    async def subscribe(self):
        pubsub = await get_pubsub()
        await pubsub.subscribe(self.CHANNEL)

        async for message in pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])
