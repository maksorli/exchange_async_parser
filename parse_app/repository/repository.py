from models.models import Spimex
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_product(self, product_data):
        product = Spimex(**product_data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)

 
    async def get_all_products(self):
 
        result = await self.db.execute(select(Spimex))
        return result.scalars().all

    async def count(self):
       
        result = await self.db.execute(select(func.count()).select_from(Spimex))
        return result.scalar_one()
    
    async def bulk_save_products(self, products_data_list):
       
       
        products = [Spimex(**data) for data in products_data_list] 
        self.db.add_all(products)  
        await self.db.commit()  