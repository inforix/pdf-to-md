import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

def get_cache(key: str) -> str:
    return redis_client.get(key)

def set_cache(key: str, value: str, expiration: int = settings.CACHE_EXPIRATION):
    redis_client.setex(key, expiration, value) 