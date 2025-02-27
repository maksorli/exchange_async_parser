import aioredis
from fastapi import FastAPI

# Настройки Redis
REDIS_URL = "redis://localhost"

async def get_redis():
    """Создание подключения к Redis"""
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis
