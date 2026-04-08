"""Connecting to redis."""
import redis.asyncio as redis
from market_data.core.config import settings


def get_redis():
    return redis.Redis(host=settings.REDIS_HOST, port=6379)
