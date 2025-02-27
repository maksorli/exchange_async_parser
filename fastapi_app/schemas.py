from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime, date


class TradingResults(BaseModel):
 
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: datetime  
    created_on: datetime  
    updated_on: datetime  

class TradingDays(BaseModel):
    n: int

class TradingDynamicsRequest(BaseModel):
    oil_id: Optional[str] = Field(None, description="Идентификатор нефти")
    delivery_type_id: Optional[str] = Field(None, description="Тип поставки")
    delivery_basis_id: Optional[str] = Field(None, description="База поставки")
    start_date: Optional[date] = Field(None, description="Дата начала периода")
    end_date: Optional[date] = Field(None, description="Дата окончания периода")

# Модель ответа
class TradingDynamicsResponse(BaseModel):
    date: datetime
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str
    volume: int
    total: int
    count: int