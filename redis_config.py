import aioredis
from aioredis import Redis
from config import BROKER_URL


redis: Redis or None = None


async def get_redis() -> Redis:
    global redis
    if redis is None:
        redis = await aioredis.from_url(BROKER_URL, encoding="utf-8", decode_responses=True)
    return redis


async def close_redis():
    global redis
    if redis:
        await redis.close()
        redis = None
