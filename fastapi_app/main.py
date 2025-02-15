from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base import get_db
from repository.models import Spimex

app = FastAPI(title="SPIMEX API")

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI работает отдельно!"}

@app.get("/results/")
async def get_trading_results(db: AsyncSession = Depends(get_db)):
    """Получение всех записей из таблицы spimex_trading_results"""
    result = await db.execute("SELECT * FROM spimex_trading_results")
    return result.fetchall()
