from sqlalchemy import select, Result, insert, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

class BaseRepository:
    model = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result: Result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result: Result  = await self.session.execute(query)
        return result.scalars().one_or_none()

    
    async def add(self, schemas: BaseModel):
        add_hotel_stmt = insert(self.model).values(**schemas.model_dump()).returning(self.model)
        result: Result = await self.session.execute(add_hotel_stmt)
        res = result.scalars().one()
        return res
    
        
   
        
        
        