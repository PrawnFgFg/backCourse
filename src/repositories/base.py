from sqlalchemy import select, Result, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

class BaseRepository:
    model = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_query(self, **filter_by):
        check_query = await self.get_all(**filter_by)
        
        if len(check_query) > 1:
            raise SQLAlchemyError("Ошибка 422 - 2 и более объектов")
        if len(check_query) == 0:
            raise SQLAlchemyError("Ошибка 404 - объект не найден")
        
        
    
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
        print("schema", schemas)
        print("**schemas.model_dump()", schemas.model_dump())
        return res
    
        
    async def edit(self, schemas: BaseModel, exclude_unset: bool = False, **filter_by):
        
        await self.check_query(**filter_by)
        
        put_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**schemas.model_dump(exclude_unset=exclude_unset))
            )
        result: Result = await self.session.execute(put_stmt)
        return {"status": "Ok"}
        
    
    
    async def delete(self, **filter_by) -> None:
        
        await self.check_query(**filter_by)
        
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(delete_stmt)
        return {"status": "Ok"}


        
