import pytest
from fastapi_app.repository.api_repository import SpimexRepository
from sqlalchemy import text
@pytest.mark.asyncio
async def test_get_last_trading_dates_returns_correct_number(db):
    dates = await SpimexRepository.get_last_trading_dates(3, db)
    assert len(dates) == 3

@pytest.mark.asyncio
async def test_get_last_trading_dates_returns_dates_in_descending_order(db):
    dates = await SpimexRepository.get_last_trading_dates(5, db)
    assert dates == sorted(dates, reverse=True)

@pytest.mark.asyncio
async def test_get_last_trading_dates_empty_db(db):
    await db.execute(text('DELETE FROM spimex_trading_results;'))
    #await db.commit()

    dates = await SpimexRepository.get_last_trading_dates(5, db)
    assert dates == []
