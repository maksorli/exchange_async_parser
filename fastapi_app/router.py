from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from models.base import get_db
from repository.api_repository import SpimexRepository
from schemas import TradingResults, TradingDays, TradingDynamicsResponse
from utils import get_seconds_until_14_11
from fastapi_cache import FastAPICache
import logging
import aioredis
import random
from fastapi import Response
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Торги"],
)


@router.get("/trading_results")
@cache(expire=lambda: get_seconds_until_14_11(), namespace="trading_results")
async def get_all(db: AsyncSession = Depends(get_db))-> list[TradingResults]:
    logger.info("Запрос к /trading_results")

    records = await SpimexRepository.get_trading_results(db)
      
    return records




@router.post("/get_last_trading_dates")
@cache(expire=lambda: get_seconds_until_14_11(), namespace="get_last_trading_dates")
async def get_all(request: TradingDays, db: AsyncSession = Depends(get_db))-> list[TradingResults]:
    return await SpimexRepository.get_last_trading_dates(request.n, db)


@router.post("/get_dynamics", response_model=List[TradingDynamicsResponse])
@cache(expire=lambda: get_seconds_until_14_11(), namespace="get_last_trading_dates")
async def get_trading_dynamics(
    request: TradingResults,
    db: AsyncSession = Depends(get_db),
):
    data = await SpimexRepository.get_dynamics(db, request)
    return data  # Pydantic автоматически преобразует ORM-объекты в JSON-ответ


@router.get("/check-cache")
async def check_cache():
    redis: aioredis.Redis = FastAPICache.get_backend().redis
    keys = await redis.scan(match="fastapi-cache:trading_results*")  # Ищем все ключи с namespace
    return {"cache_keys": keys[1]}  # Второй элемент - список найденных ключей

@router.get("/debug-redis-keys")
async def debug_redis_keys():
    redis: aioredis.Redis = FastAPICache.get_backend().redis
    keys = await redis.scan(match="*")  # Получаем все ключи
    return {"all_keys": keys}

from fastapi import Response
from fastapi_cache import FastAPICache
import aioredis
import random

@router.get("/test-cache")
@cache(expire=10, namespace="test")
async def test_cache(response: Response):
    cache_backend = FastAPICache.get_backend().redis
    cache_key = "fastapi-cache:test"

    # Проверяем, есть ли кэш
    cached_value = await cache_backend.get(cache_key)
    if cached_value:
        response.headers["x-fastapi-cache"] = "HIT"
    else:
        response.headers["x-fastapi-cache"] = "MISS"

    return {"random_number": random.randint(1, 100000)}
