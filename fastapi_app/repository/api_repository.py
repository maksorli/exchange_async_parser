from models.base import AsyncSession
from sqlalchemy.future import select
from models.models import Spimex 
from schemas import TradingResults, TradingDynamicsRequest
from sqlalchemy import func
import logging
from typing import List
from datetime  import datetime
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SpimexRepository:
    @classmethod
    async def find_all(cls, db: AsyncSession)-> list[TradingResults]:
        """Получение всех записей из таблицы spimex_trading_results"""
        result = await db.execute(select(Spimex).limit(500))
        return result.scalars().all()  

    @classmethod
    async def get_last_trading_dates(cls, n:int, db:AsyncSession ):       # – список дат последних торговых дней (фильтрация по кол-ву последних торговых дней).
        
            stmt = select(Spimex.date).distinct().order_by(Spimex.date.desc()).limit(n)
            result = await db.execute(stmt)       
            return result.scalars().all()
    
 
    
    @classmethod
    async def get_trading_results(cls, db: AsyncSession)-> list[TradingResults]: #– список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
   
        logger.info("Запрос данных из базы данных До кэширования")
        last_date_result = await db.execute(select(func.max(Spimex.date)))
        last_date = last_date_result.scalar()

        if not last_date:
            return []

        
        result = await db.execute(select(Spimex).where(Spimex.date == last_date))
        return result.scalars().all()
    
 
    @classmethod
    async def get_dynamics(    #– список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
        cls,
        db: AsyncSession,
        request: TradingDynamicsRequest
    ) -> List[TradingResults]:
        stmt = select(Spimex).order_by(Spimex.date)

 
        if request.oil_id:
            stmt = stmt.filter(Spimex.oil_id == request.oil_id)
        if request.delivery_type_id:
            stmt = stmt.filter(Spimex.delivery_type_id == request.delivery_type_id)
        if request.delivery_basis_id:
            stmt = stmt.filter(Spimex.delivery_basis_id == request.delivery_basis_id)
        if request.start_date:
            stmt = stmt.filter(Spimex.date >= request.start_date)
        if request.end_date:
            stmt = stmt.filter(Spimex.date <= request.end_date)

 
        result = await db.execute(stmt)
        return result.scalars().all()