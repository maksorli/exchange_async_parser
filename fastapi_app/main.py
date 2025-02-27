from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
# from models.base import get_db
# from models.models import Spimex
from contextlib import asynccontextmanager
from router import router  as trading_router
import aioredis
app = FastAPI(title="SPIMEX API")

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает отдельно!"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://redis_cache:6379")
    await redis.ping()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info(">>> Кэширование инициализировано")
    yield
    print("Конец работы fastapi")
app = FastAPI(lifespan=lifespan)
app.include_router(trading_router)