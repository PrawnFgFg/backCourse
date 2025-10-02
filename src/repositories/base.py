from sqlalchemy import select, Result, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, ResourceClosedError
from fastapi import HTTPException, status
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper
from src.execptions import ObjectNotFoundError


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_query(self, **filter_by):
        check_query = await self.get_one_or_none(**filter_by)
        if check_query is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Объект не найден")

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)

        result: Result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entithy(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entithy(model)
    
    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundError
        return self.mapper.map_to_domain_entithy(model)

    async def add(self, schemas: BaseModel):
        add_hotel_stmt = insert(self.model).values(**schemas.model_dump()).returning(self.model)
        result: Result = await self.session.execute(add_hotel_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entithy(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_hotel_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_hotel_stmt)

    async def edit(self, schemas: BaseModel, exclude_unset: bool = False, **filter_by):
        # await self.check_query(**filter_by)

        put_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**schemas.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result: Result = await self.session.execute(put_stmt)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundError
        return self.mapper.map_to_domain_entithy(model)

    async def delete(self, **filter_by) -> None:
        # res = await self.check_query(**filter_by)
        # print(res)

        delete_stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(delete_stmt)
        try:
            result = res.scalar_one() 
        except ResourceClosedError:
            raise ObjectNotFoundError
        return None

    async def delete_bulk(self, *filter, **filter_by):
        delete_stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(delete_stmt)
        return {"status": "Ok"}
