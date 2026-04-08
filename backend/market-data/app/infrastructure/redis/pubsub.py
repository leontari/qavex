"""Redis client wrapper."""
from market_data.infrastructure.redis.client import get_redis


async def get_pubsub():
    redis = get_redis()
    return redis.pubsub()
