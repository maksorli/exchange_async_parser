from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from models.base import get_db
from repository.api_repository import SpimexRepository
from schemas import TradingResults, TradingDays, TradingDynamicsRequest
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


@router.get("/trading_results", response_model=List[TradingResults])
@cache(expire=lambda: get_seconds_until_14_11(), namespace="last_trading_results")
async def last_trading_results(db: AsyncSession = Depends(get_db))-> list[TradingResults]:
    logger.info("Запрос к /trading_results")

    records = await SpimexRepository.get_trading_results(db)
      
    return records




@router.post("/get_last_trading_dates")
@cache(expire=lambda: get_seconds_until_14_11(), namespace="get_last_trading_dates")
async def get_last_trading_dates(request: TradingDays, db: AsyncSession = Depends(get_db))-> list[TradingResults]:
    return await SpimexRepository.get_last_trading_dates(request.n, db)


@router.post("/get_dynamics", response_model=List[TradingResults])
@cache(expire=lambda: get_seconds_until_14_11(), namespace="get_last_trading_dates")
async def get_trading_dynamics(
    request: TradingDynamicsRequest,
    db: AsyncSession = Depends(get_db),
)-> list[TradingResults]:
    data = await SpimexRepository.get_dynamics(db, request)
    return data  # Pydantic автоматически преобразует ORM-объекты в JSON-ответ


