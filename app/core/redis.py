from typing import Union

from redis.asyncio import Redis, ConnectionPool

from app.core.config import settings

redis_client: Union[Redis, None] = None


def get_redis_pool():
    if redis_client is None:
        raise ValueError()
    return redis_client


async def init_redis():
    global redis_client
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=2,
        max_connections=20,
        decode_responses=True
    )
    redis_client = Redis(
        connection_pool=pool
    )
    await redis_client.ping()


async def close_redis_pool():
    global redis_client
    if redis_client:
        await redis_client.aclose()
