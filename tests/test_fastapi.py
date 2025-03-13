import pytest
from unittest.mock import AsyncMock, Mock
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_app.router import router
from fastapi import FastAPI
from models.base import get_db


@pytest.fixture
def mock_db():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = Mock()
   
    mock_result.scalars.return_value = mock_scalars = Mock()
    mock_scalars.all.return_value = [date(2024, 3, 12), date(2024, 3, 11), date(2024, 3, 10)]

    mock_session.execute.return_value = mock_result
    mock_result.scalars.return_value = mock_scalars

    return mock_session


@pytest.fixture
def client(mock_db):
    app = FastAPI()

  
    from unittest.mock import patch
    with patch('fastapi_app.router.cache', lambda *args, **kwargs: lambda f: f):
        app.include_router(router)

 
    app.dependency_overrides[get_db] = lambda: mock_db

    with TestClient(app) as client:
        yield client


def test_get_last_trading_dates_endpoint(client):
    response = client.post("/api/get_last_trading_dates", json={"n": 3})

    assert response.status_code == 200
    assert response.json() == ["2024-03-12", "2024-03-11", "2024-03-10"]
