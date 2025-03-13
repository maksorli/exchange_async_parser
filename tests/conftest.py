import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

TEST_DATABASE_URL = "postgresql+asyncpg://em3_user:password@localhost:5435/testdb"

engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db():
    async with async_session_maker() as session:
        yield session
        await session.rollback()  # Откатываем транзакцию после каждого теста
